import streamlit as st

from sources.data_plotting import plot_data
from sources.data_process import convert_to_probabilities
from sources.data_retriever import get_data, cache
from sources.locations import Locations
from sources.variables import Variables


def run_case(location: Locations, variable: Variables):
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

    st.pyplot(fig=figure)


def main():
    st.title("Weather Probability App!")
    st.sidebar.title("Select Variable and Place")
    loc = st.sidebar.selectbox("Locations", [_loc.name.capitalize() for _loc in Locations])
    var = st.sidebar.selectbox("Variable", [_var.name.capitalize() for _var in Variables])

    with st.spinner(text="..."):
        st.subheader(str(var).capitalize())
        run_case(Locations[loc.lower()], Variables[var.lower()])


if __name__ == "__main__":
    main()
