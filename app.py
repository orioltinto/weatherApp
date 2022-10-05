import streamlit as st

from sources.data_plotting import plot_data
from sources.data_process import convert_to_probabilities
from sources.data_retriever import get_data, cache
from sources.location_retriever import location_widget
from sources.models import Models
from sources.variables import Variables


def run_case(location: int, variable: Variables, model: Models):
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
    st.sidebar.title("Select Location:")
    loc_name, loc_id = location_widget()
    st.sidebar.markdown("---")
    st.sidebar.title("Select Variable:")
    var = st.sidebar.selectbox("Variable", [_var.name.capitalize() for _var in Variables])
    st.sidebar.markdown("---")
    st.sidebar.title("Select Model:")
    model = st.sidebar.selectbox("Model", [_mod.name.capitalize() for _mod in Models])
    st.sidebar.markdown("---")

    st.subheader(f"{str(var).capitalize()} at {str(loc_name)}")

    with st.spinner():
        try:
            run_case(loc_id, Variables[var.lower()], Models[model.lower()])
        except AssertionError as err:
            st.warning(err)
    st.markdown(f"Model: {str(model).capitalize()}")


if __name__ == "__main__":
    main()
