import locale
import logging
import os
import platform


import click
import colorama
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# import plotly.graph_objects as go
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

from housing_prices.config import Config
from housing_prices import helpers

# Most users should depend on colorama >= 0.4.6, and use just_fix_windows_console().
colorama.just_fix_windows_console()
# Set the locale to the user's default setting
locale.setlocale(locale.LC_ALL, "")
# Set the documentation URL for make_rst_to_ansi_formatter()
doc_url = "https://hakonhagland.github.io/pyml-regressions-example1/main/index.html"
# CLI colors for make_rst_to_ansi_formatter()
cli_colors = {
    "heading": {"fg": colorama.Fore.GREEN, "style": colorama.Style.BRIGHT},
    "url": {"fg": colorama.Fore.CYAN, "style": colorama.Style.BRIGHT},
    "code": {"fg": colorama.Fore.BLUE, "style": colorama.Style.BRIGHT},
}
click_command_cls = make_rst_to_ansi_formatter(doc_url, colors=cli_colors)

np.random.seed(42)  # make the output stable across runs
plt.rc("font", size=12)
plt.rc("axes", labelsize=14, titlesize=14)
plt.rc("legend", fontsize=12)
plt.rc("xtick", labelsize=10)
plt.rc("ytick", labelsize=10)
# Check for a display (relevant for Linux)
if platform.system() != "Windows":  # pragma: no cover
    if os.environ.get("DISPLAY") is None:
        # Set to a non-interactive backend if there's no display, e.g. GitHub Actions
        matplotlib.use("Agg")


@click.group(cls=make_rst_to_ansi_formatter(doc_url, group=True, colors=cli_colors))
@click.option("--verbose", "-v", is_flag=True, help="Show verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """``housing-prices`` let's you explore the housing price data presented in Chapter 2 of the book
    `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3rd ed.) <https://github.com/ageron/handson-ml3>`_.

    The following subcommands are available:

    * ``download-data``: Download the housing price data from the book's web page.

    * ``info``: Print information about the housing price data.

    * ``describe-column``: Print information about a specific column in the housing price data.

    """
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        # logging.basicConfig(level=logging.WARNING)


@main.command(cls=click_command_cls)
def download_data() -> None:
    """``housing-prices download-data`` downloads the housing price data from
    `the book's web page <https://github.com/ageron/data>`_.
    """
    config = Config()
    datadir = config.get_data_dir()
    helpers.download_data(datadir)


@main.command(cls=click_command_cls)
def info() -> None:
    """``housing-prices info`` prints information about the housing price data."""
    config = Config()
    housing = helpers.get_housing_data(config, download=True)
    if housing is not None:
        housing.info()
        local_path = helpers.get_housing_local_path(config)
        print(f"Data file path: {local_path}")


@main.command(cls=click_command_cls)
@click.argument("column-name", type=str)
def describe_column(column_name: str) -> None:
    """``housing-prices describe-column`` prints information about a specific column. See
    ``housing-prices info`` for information about the housing price column names."""
    config = Config()
    housing = helpers.get_housing_data(config, download=True)
    if housing is not None:
        print(housing[column_name].describe())


@main.command(cls=click_command_cls)
def plot_histograms() -> None:
    """``housing-prices plot-histograms`` plots histograms of the housing price data."""
    config = Config()
    housing = helpers.get_housing_data(config, download=True)
    if housing is not None:
        housing.hist(bins=50, figsize=(20, 15))
        plt.show()  # type: ignore
