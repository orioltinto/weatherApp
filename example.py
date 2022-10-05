from joblib import Parallel, delayed
from tqdm import tqdm

# Change matplotlib backend
from sources.data_plotting import plot_data, save_figure
from sources.data_process import convert_to_probabilities
from sources.data_retriever import get_data, cache
from sources.locations import Locations
from sources.models import Models
from sources.variables import Variables


def main():
    # Create a list with all cases
    cases = [(location, variable, model) for location in Locations for variable in Variables for model in Models]

    Parallel(n_jobs=-2)(delayed(run_case)(location, variable, model) for location, variable, model in tqdm(cases))
    """
    for case in tqdm(cases):
        location, variable, model = case
        # Get the data
        try:
            run_case(location, variable, model)
        except AssertionError:
            pass
    """


def run_case(location: Locations, variable: Variables, model: Models):
    try:
        is_new, data = get_data(location, variable, model)
    except AssertionError:
        return

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
    save_figure(figure, plots_folder / f"{model.name}_{location.name}_{variable.name}.png")


if __name__ == "__main__":
    from pathlib import Path

    plots_folder = Path("plots")
    if not plots_folder.exists():
        plots_folder.mkdir()

    main()
