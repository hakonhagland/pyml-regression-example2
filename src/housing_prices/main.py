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
from housing_prices.constants import TestSetGenMethod
from housing_prices.split_data import SplitCrc
from housing_prices import click_helpers, helpers

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


@main.command(cls=click_command_cls)
@click.option(
    "--method",
    "-m",
    callback=click_helpers.validate_test_set_gen_method,
    default="CRC",
    help="The method to use for creating the test set. Valid methods are: CRC, RANDOM, STRATIFIED",
)
@click.option(
    "--test-ratio",
    "-r",
    type=float,
    default=0.2,
    help="The ratio of the test set size to the full dataset size. Default is 0.2",
)
def create_test_set(method: TestSetGenMethod, test_ratio: float) -> None:
    """``housing-prices create-test-set`` creates a test set from the housing price data.
    The default splitting ``--method`` is to use a ``CRC`` (Cyclic Redundancy Check) to split the data.
    The other methods (not implemented yet) are ``RANDOM`` and ``STRATIFIED``. Method names can
    be given in lowercase or uppercase. Short names are also accepted,
    e.g. ``RND`` for ``RANDOM``, and ``STR`` for STRATIFIED. The test set ratio can be set with
    the ``--test-ratio`` option. The default ratio is 0.2. The test ratio is the ratio of the test
    set size to the full dataset size.
    """
    config = Config()
    housing = helpers.get_housing_data(config, download=True)
    if housing is not None:
        if method == TestSetGenMethod.CRC:
            SplitCrc(housing, config).split_data(test_ratio)
        else:
            raise NotImplementedError(
                f"Test set generation method {method.value} not implemented yet"
            )
