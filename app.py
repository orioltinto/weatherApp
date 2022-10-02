import streamlit as st

from main import Locations, Variables, get_data, convert_to_probabilities, plot_data, cache, cache_file_path


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
        figure = plot_data(prob_data)
        cache.figures[(location, variable)] = figure
    else:
        figure = cache.figures[(location, variable)]

    print(f"{figure=}")
    st.pyplot(fig=figure)
    print(cache.figures)
    # Save cache for future usage
    cache.save_cache(cache_file_path)


def main():
    st.title("Weather Probability App!")
    st.sidebar.title("Select Variable and Place")
    loc = st.sidebar.selectbox("Locations", [_loc.name for _loc in Locations])
    var = st.sidebar.selectbox("Variable", [_var.name for _var in Variables])

    with st.spinner(text="..."):
        st.subheader(str(var).capitalize())
        run_case(Locations[loc], Variables[var])


if __name__ == "__main__":
    main()
    print("ending")
