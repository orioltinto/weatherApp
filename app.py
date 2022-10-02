import streamlit as st

from main import Locations, Variables, get_data, convert_to_probabilities, plot_data


def run_case(location: Locations, variable: Variables):
    # Get the data
    data = get_data(location, variable)
    # Convert the data
    prob_data = convert_to_probabilities(data, variable)
    figure = plot_data(prob_data)
    st.pyplot(fig=figure, clear_figure=True)


def main():
    st.title("Weather Probability App!")
    st.sidebar.title("Select Variable and Place")
    loc = st.sidebar.selectbox("Locations", [_loc.name for _loc in Locations])
    var = st.sidebar.selectbox("Variable", [_var.name for _var in Variables])

    with st.spinner(text="Computing..."):
        st.subheader(str(var).capitalize())
        run_case(Locations[loc], Variables[var])


if __name__ == "__main__":
    main()
    print("ending")
