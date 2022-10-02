from pathlib import Path
from typing import Union

import matplotlib
import numpy as np
import xarray
from matplotlib import pyplot as plt

matplotlib.use("Agg")

COLORMAP = "Blues"


def tick_to_label(hours_since_start: int) -> str:
    days = hours_since_start // 24
    hours = hours_since_start % 24
    return f"+{days}d {hours}h" if days else f"{hours}h"


def plot_data(data_array: xarray.DataArray):
    data_array.T.plot.contourf(levels=np.linspace(0, 100, 11), cmap=COLORMAP)
    ticks = range(min(data_array.time.values), max(data_array.time.values), 3)
    labels = [tick_to_label(t) for t in ticks]
    plt.xticks(ticks=ticks, labels=labels, rotation=45)
    return plt.gcf()


def save_figure(figure: matplotlib.figure, filename: Union[Path, str]):
    filename = Path(filename).resolve()
    plt.figure(figure.number)
    plt.savefig(filename)
    plt.clf()
