from tqdm import tqdm

# Change matplotlib backend
from sources.data_plotting import plot_data, save_figure
from sources.data_process import convert_to_probabilities
from sources.data_retriever import get_data, cache
from sources.locations import Locations
from sources.variables import Variables


def main():
    from pathlib import Path
    plots_folder = Path("plots")
    if not plots_folder.exists():
        plots_folder.mkdir()

    location = Locations.munich

    for variable in tqdm(Variables):
        # Get the data
        is_new, data = get_data(location, variable)

        # Convert the data
        if is_new:
            prob_data = convert_to_probabilities(data, variable)
            cache.probabilities[(location, variable)] = prob_data
        else:
            prob_data = cache.probabilities[(location, variable)]
        if is_new:
            figure = plot_data(data, prob_data)
            cache.figures[(location, variable)] = figure
        else:
            figure = cache.figures[(location, variable)]
        save_figure(figure, plots_folder / f"{variable.name}.png")


if __name__ == "__main__":
    main()
