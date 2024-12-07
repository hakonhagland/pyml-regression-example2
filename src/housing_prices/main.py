import locale
import logging
import os
import platform


import click
import colorama
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# import plotly.graph_objects as go
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

from housing_prices.config import Config
from housing_prices.constants import TestSetGenMethod
from housing_prices.split_data import SplitCrc, SplitStratified
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

    * ``create-test-set`` : Create a test set from the housing price data.

    * ``describe-column`` : Print information about a specific column in the housing price data.

    * ``download-data``   : Download the housing price data from the book's web page.

    * ``info``            : Print information about the housing price data.

    * ``plot-histograms`` : Plot histograms of the housing price data.

    * ``stratify-column`` : Stratify the data in a column of the housing price data.

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
        local_path = config.get_housing_local_path()
        print(f"Data file path: {local_path}")


@main.command(cls=click_command_cls)
@click.argument("column-name", type=str)
def describe_column(column_name: str) -> None:
    """``housing-prices describe-column`` prints information about a specific column. See
    ``housing-prices info`` for information about the housing price column names."""
    config = Config()
    housing = helpers.get_housing_data(config, download=True)
    if housing is not None:
        # Check if the column name is valid
        if column_name not in housing.columns:
            logging.error(
                f"Invalid column name '{column_name}'. Valid column names are: {housing.columns}"
            )
            return
        print(housing[column_name].describe())


@main.command(cls=click_command_cls)
@click.option(
    "--column-name",
    "-c",
    type=str,
    help="The column name to plot. If not given, all columns are plotted. A list of valid column names can be obtained with the ``housing-prices info`` command.",
)
def plot_histograms(column_name: str | None) -> None:
    """``housing-prices plot-histograms`` plots histograms of the housing price data."""
    config = Config()
    housing = helpers.get_housing_data(config, download=True)
    if housing is not None:
        if column_name:
            housing[column_name].hist(bins=50, figsize=(20, 15))
            extra_label_info = helpers.get_extra_col_name_info(column_name)
            col_name_str = (
                column_name.replace("_", " ") if column_name else "all columns"
            )
            plt.title(f"Histogram of {col_name_str}")
            col_name_str += extra_label_info
            col_name_str = col_name_str.capitalize()
            plt.xlabel(f"{col_name_str}")
            plt.ylabel("Frequency")
        else:
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
@click.option(
    "--stratify-column",
    "-c",
    type=str,
    help="The column to stratify the data on. Column must be prepared in advance with the ``stratify-column`` command.",
)
def create_test_set(
    method: TestSetGenMethod, test_ratio: float, stratify_column: str
) -> None:
    """``housing-prices create-test-set`` creates a test set from the housing price data.
    The default splitting ``--method`` is to use a ``CRC`` (Cyclic Redundancy Check) to split the data.
    Stratified splitting can also be used with the ``STRATIFIED`` method. It requires a column name
    to stratify the data on. It is assumed that the column has been prepared in advance with the ``stratify-column`` command.
    The ``RANDOM`` method is not implemented yet. Method names can
    be given in lowercase or uppercase. Short names are also accepted,
    e.g. ``RND`` for ``RANDOM``, and ``STR`` for STRATIFIED. The test set ratio can be set with
    the ``--test-ratio`` option. The default ratio is 0.2. The test ratio is the ratio of the test
    set size to the full dataset size. If method is ``STRATIFIED``, the ``--stratify-column`` option
    can be used to specify the column to stratify the data on. See ``housing-prices stratify-column``
    """
    config = Config()
    housing = helpers.get_housing_data(config, download=True)
    if housing is not None:
        if method == TestSetGenMethod.CRC:
            SplitCrc(housing, config).split_data(test_ratio)
        elif method == TestSetGenMethod.STRATIFIED:
            if stratify_column is None:
                logging.error(
                    "The STRATIFIED method requires a column name for stratification."
                )
                return
            SplitStratified(housing, config).split_data(test_ratio, stratify_column)
        else:
            raise NotImplementedError(
                f"Test set generation method {method.value} not implemented yet"
            )


@main.command(cls=click_command_cls)
@click.argument("column-name", type=str)
@click.option(
    "--bins",
    "-b",
    required=True,
    type=str,
    callback=click_helpers.validate_bins,
    help="Comma-separated list of bin edges. The number of bins is one less than the number of bin edges.",
)
def stratify_column(column_name: str, bins: list[float]) -> None:
    """``housing-prices stratify-column COLUMN`` stratifies the data in COLUMN of the
    housing.csv data file. Use the ``--bins`` option to specify the bin edges. The number
    of bins is one less than the number of bin edges. The bin edges should be given as a
    comma-separated list of numbers. For example, ``--bins=0,100000,200000,300000`` will
    create 3 bins: [0, 100000), [100000, 200000), [200000, 300000). See ``housing-prices info``
    for information about the housing price column names, and ``housing-prices describe-column``
    for information about the minimum and maximum column values. The strafified data bins are
    labeled with consequtive integers starting from 1. Finally, the stratified data is plotted
    as a histogram."""
    config = Config()
    housing = helpers.get_housing_data(config, download=True)
    if housing is not None:
        # Check if the column name is valid
        if column_name not in housing.columns:
            logging.error(
                f"Invalid column name '{column_name}'. Valid column names are: {housing.columns}"
            )
            return
        # Check that the minmum and maximum values are within the bin edges
        min_val = housing[column_name].min()
        max_val = housing[column_name].max()
        if min_val < bins[0] or max_val > bins[-1]:
            logging.error(
                f"Column values must be within the bin edges. Got min: {min_val}, max: {max_val}, bins: {bins}"
            )
            return
        # Assign labels 1,2,3,... to the bins
        labels = np.arange(1, len(bins), 1)
        stratified = pd.cut(housing[column_name], bins, labels=labels)  # type: ignore
        helpers.save_stratified_column(config, column_name, stratified, bins)
        fig, ax = plt.subplots()
        bin_counts = stratified.value_counts().sort_index()
        bars = ax.bar(
            bin_counts.index.astype(float),
            bin_counts.values,
            tick_label=bin_counts.index,
        )

        # ax = stratified.value_counts().sort_index().plot(kind="bar", rot=0, grid=True)

        # Generate bin legends
        legends = [
            f"bin {i + 1}: [{bins[i]}, {bins[i + 1]}]" for i in range(len(bins) - 1)
        ]
        # Assign legends to each bar
        for bar, legend in zip(bars, legends):
            bar.set_label(legend)

        # breakpoint()
        # Add legends to the plot
        ax.legend(title="Bins", handlelength=0)
        column_name = column_name.capitalize()
        ax.set_title(column_name.replace("_", " "))
        ax.set_xlabel("Bins")
        ax.set_ylabel("Frequency")
        plt.show()  # type: ignore
