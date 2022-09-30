import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Tuple

import matplotlib
import numpy as np
import requests
import xarray
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from tqdm import tqdm

# Change matplotlib backend
matplotlib.use("Agg")

COLORMAP = "Blues"


class AvailableLocations(Enum):
    Munich = "2867714"


class AvailableVariables(Enum):
    precipitation = "niederschlag"
    accumulated_precipitation = "niederschlagssumme"
    temperature = "temperatur"
    humidity = "relfeuchte"
    dew_point = "taupunkt"
    pressure = "luftdruck"


def download_page(location: AvailableLocations, variable: AvailableVariables) -> requests.Response:
    URL = "https://meteologix.com/uk/ajax/ensemble"
    REFERER = "https://meteologix.com/uk/forecast/2867714-munich/ensemble/rapid-id2/precipitation"

    REQUEST_PARAMS = {"city_id": location.value,
                      "model": "rapid-id2",
                      "model_view": "",
                      "param": variable.value,
                      }
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        "referer": REFERER,

    }

    return requests.get(URL, headers=HEADERS, params=REQUEST_PARAMS)


def parse_page(page: requests.Response) -> dict:
    # Parse with BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')
    # Get script part
    script = soup.find(type="text/javascript").extract().string

    # Look for the variable that contains the data
    search_for = "var hcensemblelong_data = "

    # Split script in lines
    script_lines = script.split("\n")

    # Look for the first line
    start = [index for index, line in enumerate(script_lines) if line.count(search_for)][0]

    # Until the end
    data_lines = script_lines[start:]

    # FIXME: The data is in a json format but with some things that need fixing.
    #  A cleaner way of getting this done would be nice.
    data_in_json_format = "\n".join(data_lines)

    # Remove the variable declaration in the first line
    data_in_json_format = data_in_json_format.replace(search_for, "")
    # Make sure that only double commas are used
    data_in_json_format = data_in_json_format.replace("'", '"')
    # Remove last ;
    data_in_json_format = data_in_json_format.strip()[:-1]
    # Fix trailing comma problem. Spaces are important here.
    data_in_json_format = data_in_json_format.replace('                                "enabled": false,',
                                                      '                                "enabled": false')

    # After the fix, parse the data and convert it to a dictionary
    parsed_data = json.loads(data_in_json_format)

    return parsed_data


def extract_variable_information(parsed_data: dict) -> xarray.DataArray:
    # Extract the member data from the parsed data
    data_dictionary = {}
    for member in parsed_data:
        data_dictionary[member["name"]] = member["data"]

    # Get list of members
    members = list(data_dictionary.keys())

    def get_time_and_variable(member_data: dict) -> Tuple[list, list]:
        """
        Function to extract time and data values from data corresponding to a single member.
        :param member_data:
        :return:
        """
        time = [datetime.fromtimestamp(d[0] / 1000) for d in member_data]
        values = [d[1] for d in member_data]
        return time, values

    # Get the data shape to create an empty array
    times, var = get_time_and_variable(data_dictionary[members[0]])

    data_shape = (len(members), len(times))
    data = np.zeros(data_shape)

    # Process all members to fill the array.
    for m_idx, member in enumerate(members):
        times, var = get_time_and_variable(data_dictionary[member])
        data[m_idx, :] = var

    # Convert numpy array to data array with the corresponding dimensions
    dataArray = xarray.DataArray(data, coords={"member": members, "time": times})

    return dataArray


def get_data(location: AvailableLocations, variable: AvailableVariables) -> xarray.DataArray:
    # Download webpage
    page = download_page(location, variable)
    # Parse the webpage and obtain a dictionary
    parsed_data = parse_page(page)

    # Extract the relevant information as a data array
    dataArray = extract_variable_information(parsed_data)

    return dataArray


def convert_to_probabilities(data_array: xarray.DataArray, variable: AvailableVariables) -> xarray.DataArray:
    """
    Given a data array containing a dimension member and a dimension time, create a new dataset in which
    the new dimensions are the time and the variable value, and the actual values are the
    probabilities of that happening.
    :param data_array:
    :param variable:
    :return data_array:
    """
    min_value = data_array.min().values
    max_value = data_array.max().values
    number_of_steps = 100
    steps = np.linspace(min_value, max_value, number_of_steps)
    times = data_array["time"]
    number_of_members = data_array["member"].size
    prob_array = np.zeros((len(times), len(steps)))

    for t_idx, t in enumerate(times):
        for s_idx, s in enumerate(steps):
            prob_array[t_idx, s_idx] = (data_array.sel(time=t) > s).sum() / number_of_members * 100.
    prob_dataArray = xarray.DataArray(prob_array, coords={"time": times.astype(float), variable.name: steps})
    return prob_dataArray


def plot_data(data_array: xarray.DataArray, file_name: Path = None) -> None:
    plot = data_array.T.plot.contourf(levels=np.linspace(0, 100, 11), cmap=COLORMAP)
    if file_name is not None:
        plt.title("Probabilities")
        plt.savefig(file_name)
        plt.clf()
    return plot


def main():
    from pathlib import Path
    plots_folder = Path("plots")
    if not plots_folder.exists():
        plots_folder.mkdir()

    location = AvailableLocations.Munich
    for variable in tqdm(AvailableVariables):
        # Get the data
        data = get_data(location, variable)
        # Convert the data
        prob_data = convert_to_probabilities(data, variable)
        plot_data(prob_data, plots_folder / f"{variable.name}.png")


if __name__ == "__main__":
    main()
