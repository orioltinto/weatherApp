import streamlit as st
import hvplot as hv
import hvplot.xarray  # noqa

from main import AvailableLocations, AvailableVariables, get_data, convert_to_probabilities, plot_data


def run_case(location: AvailableLocations, variable: AvailableVariables):
    # Get the data
    data = get_data(location, variable)
    # Convert the data
    prob_data = convert_to_probabilities(data, variable)
    plot = prob_data.T.hvplot.contourf()
    plot.opts(invert_axes=True)
    st.bokeh_chart(hv.render(plot, backend='bokeh'))


def main():
    st.title("Weather Probability App!")
    st.sidebar.title("Select Variable and Place")
    loc = st.sidebar.selectbox("Locations", [_loc.name for _loc in AvailableLocations])
    var = st.sidebar.selectbox("Variable", [_var.name for _var in AvailableVariables])

    if st.sidebar.button("Run"):
        with st.spinner(text="Computing..."):
            st.subheader(var)
            run_case(AvailableLocations[loc], AvailableVariables[var])


if __name__ == "__main__":
    main()
    print("ending")
