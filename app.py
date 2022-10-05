import streamlit as st

from sources.data_plotting import plot_data
from sources.data_process import convert_to_probabilities
from sources.data_retriever import get_data, cache
from sources.locations import Locations
from sources.models import Models
from sources.variables import Variables


def run_case(location: Locations, variable: Variables, model: Models):
    # Get the data
    is_new, data = get_data(location, variable, model)

    # Convert the data
    if is_new:
        prob_data = convert_to_probabilities(data, variable)
        cache.probabilities[(location, variable, model)] = prob_data
    else:
        prob_data = cache.probabilities[(location, variable, model)]
    if is_new:
        figure = plot_data(data, prob_data)
        cache.figures[(location, variable, model)] = figure
    else:
        figure = cache.figures[(location, variable, model)]

    st.pyplot(fig=figure)


def main():
    st.set_page_config(
        page_title="Weather Probability App!",
    )
    st.title("Weather Probability App!")
    st.sidebar.title("Select Variable and Place")
    loc = st.sidebar.selectbox("Locations", [_loc.name.capitalize() for _loc in Locations])
    var = st.sidebar.selectbox("Variable", [_var.name.capitalize() for _var in Variables])
    model = st.sidebar.selectbox("Model", [_mod.name.capitalize() for _mod in Models])
    st.subheader(f"{str(var).capitalize()} at {str(loc).capitalize()}. Model: {str(model).capitalize()}")
    try:
        run_case(Locations[loc.lower()], Variables[var.lower()], Models[model.lower()])
    except AssertionError as err:
        st.warning(err)


if __name__ == "__main__":
    main()
