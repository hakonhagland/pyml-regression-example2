import logging
import unittest.mock

import matplotlib
import pandas as pd
import pytest
from _pytest.logging import LogCaptureFixture
from pytest_mock.plugin import MockerFixture
from click.testing import CliRunner

from housing_prices.constants import FileNames
import housing_prices.main as main
from .common import DataFileContents, MockRequestGet, PrepareConfigDir, PrepareDataDir


@pytest.mark.parametrize("verbose", [True, False])
class TestMainCmd:
    def test_help(
        self,
        verbose: bool,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_config_dir(add_config_ini=True)
        runner = CliRunner()
        args = ["download-data", "--help"]
        if verbose:
            args.insert(0, "-v")
        result = runner.invoke(main.main, args)
        assert result.stdout.startswith("Usage: main download-data [OPTIONS]")


class TestDownloadDataCmd:
    @pytest.mark.parametrize("datafile_exists", [True, False])
    def test_invoke(
        self,
        datafile_exists: bool,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
        datafile_contents: DataFileContents,
        mock_requests_get: MockRequestGet,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=datafile_exists, housing_csv=False)
        prepare_config_dir(add_config_ini=True)
        if not datafile_exists:
            file_contents = datafile_contents(FileNames.housing_tgz)
            mock_requests_get(file_contents)
        runner = CliRunner()
        args = ["download-data"]
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0


class TestInfoCmd:
    @pytest.mark.parametrize(
        "datafiles_exists",
        [True, False],
    )
    def test_invoke(
        self,
        datafiles_exists: bool,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=datafiles_exists, housing_csv=False)
        prepare_config_dir(add_config_ini=True)
        runner = CliRunner()
        args = ["info"]
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0


class TestDescribeColumnCmd:
    @pytest.mark.parametrize("invalid_column", [False, True])
    def test_invoke(
        self,
        invalid_column: bool,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True, housing_csv=False)
        prepare_config_dir(add_config_ini=True)
        runner = CliRunner()
        col_name = "total_rooms"
        if invalid_column:
            col_name = "bad_column"
        args = ["describe-column", col_name]
        result = runner.invoke(main.main, args)
        if invalid_column:
            assert caplog.records[-1].message.startswith("Invalid column name")
        else:
            assert result.exit_code == 0


class TestPlotHistogramsCmd:
    @pytest.mark.parametrize("column_name", [None, "median_income"])
    def test_invoke(
        self,
        column_name: str | None,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True, housing_csv=False)
        prepare_config_dir(add_config_ini=True)
        mock_hist = mocker.patch.object(pd.DataFrame, "hist")
        mocker.patch("matplotlib.pyplot.show", return_value=None)
        matplotlib.use("Agg")
        runner = CliRunner()
        args = ["plot-histograms"]
        if column_name:
            args.extend(["--column-name", column_name])
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0
        if column_name:
            assert True
        else:
            mock_hist.assert_called_once_with(bins=50, figsize=(20, 15))


class TestCreateTestSetCmd:
    @pytest.mark.parametrize(
        "method,bad_strat",
        [
            ["crc", False],
            ["str", False],
            ["random", False],
            ["rnd", False],
            ["bad", False],
            ["str", True],
        ],
    )
    def test_invoke(
        self,
        method: str,
        bad_strat: bool,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True, housing_csv=False, stratified_dir=True)
        prepare_config_dir(add_config_ini=True)
        runner = CliRunner()
        args = ["create-test-set", "--test-ratio", "0.2", "--method", method]
        if method == "str" and not bad_strat:
            args.extend(["--stratify-column", "median_income"])
        result = runner.invoke(main.main, args)
        if method in ["crc", "str"]:
            assert result.exit_code == 0
            if bad_strat:
                assert caplog.records[-1].message.startswith(
                    "The STRATIFIED method requires a column name"
                )
        elif method == "bad":
            assert result.exit_code == 2
        else:
            assert isinstance(result.exception, NotImplementedError)


class TestStratifyColumnCmd:
    @pytest.mark.parametrize(
        "col_name,bins_too_narrow,bins_descending,bins_nan",
        [
            ["median_income", False, False, False],
            ["bad_column", False, False, False],
            ["median_income", True, False, False],
            ["median_income", False, True, False],
            ["median_income", False, False, True],
        ],
    )
    def test_invoke(
        self,
        col_name: str,
        bins_too_narrow: bool,
        bins_descending: bool,
        bins_nan: bool,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True, housing_csv=False)
        prepare_config_dir(add_config_ini=True)
        mocker.patch("matplotlib.pyplot.show", return_value=None)
        matplotlib.use("Agg")
        runner = CliRunner()
        bins = "0,1.5,3,4.5,6,16"
        if bins_too_narrow:
            bins = "6,16,32"
        elif bins_descending:
            bins = "9,6,5,3"
        elif bins_nan:
            bins = "0,1.5,3,4.5,6,16,a"
        args = ["stratify-column", "--bins", bins, col_name]
        result = runner.invoke(main.main, args)
        if col_name == "bad_column":
            assert caplog.records[-1].message.startswith("Invalid column name")
        if bins_too_narrow:
            assert caplog.records[-1].message.startswith(
                "Column values must be within the bin edges"
            )
        elif bins_descending:
            assert result.exit_code == 2
            assert result.stdout.startswith("Usage: main stratify-column")
        elif bins_nan:
            assert result.exit_code == 2
            assert result.stdout.startswith("Usage: main stratify-column")
        else:
            assert result.exit_code == 0


class TestGeoPopScatterCmd:
    @pytest.mark.parametrize(
        "invalid_colname1,invalid_colname2",
        [[False, False], [True, False], [False, True]],
    )
    def test_invoke(
        self,
        invalid_colname1: bool,
        invalid_colname2: bool,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True, housing_csv=True)
        prepare_config_dir(add_config_ini=True)
        mock_plot = mocker.patch.object(pd.DataFrame, "plot")
        mocker.patch("matplotlib.pyplot.show", return_value=None)
        matplotlib.use("Agg")
        runner = CliRunner()
        args = ["geo-pop-scatter", "--alpha", "0.1"]
        if invalid_colname1:
            args.extend(["--column-name", "latitude"])
        elif invalid_colname2:
            args.extend(["--column-name", "bad_column"])
        result = runner.invoke(main.main, args)
        if invalid_colname1:
            assert caplog.records[-1].message.startswith("Invalid column name")
        elif invalid_colname2:
            assert caplog.records[-1].message.startswith("Invalid column name")
        else:
            assert result.exit_code == 0
            mock_plot.assert_called_once_with(
                kind="scatter",
                x="longitude",
                y="latitude",
                alpha=0.1,
                s=unittest.mock.ANY,
                figsize=(10, 7),
                c="median_house_value",
                cmap=unittest.mock.ANY,
                colorbar=True,
                sharex=False,
                label="population",
                grid=True,
            )


class TestCorrelationInfoCmd:
    @pytest.mark.parametrize("invalid_column", [False, True])
    def test_invoke(
        self,
        invalid_column: bool,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True, housing_csv=True)
        prepare_config_dir(add_config_ini=True)
        runner = CliRunner()
        args = ["correlation-info"]
        if invalid_column:
            args.append("bad_column")
        else:
            args.append("median_house_value")
        result = runner.invoke(main.main, args)
        if invalid_column:
            assert caplog.records[-1].message.startswith("Invalid column name")
        else:
            assert result.exit_code == 0


class TestScatterPlotCmd:
    @pytest.mark.parametrize(
        "cols_too_few,cols_duplicate,cols_invalid",
        [
            [False, False, False],
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ],
    )
    def test_invoke1(
        self,
        cols_too_few: bool,
        cols_duplicate: bool,
        cols_invalid: bool,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True, housing_csv=True)
        prepare_config_dir(add_config_ini=True)
        mock_plot = mocker.patch.object(pd.DataFrame, "plot")
        mocker.patch("matplotlib.pyplot.show", return_value=None)
        matplotlib.use("Agg")
        runner = CliRunner()
        args = ["scatter-plot"]
        if cols_too_few:
            args.append("median_income")
        elif cols_duplicate:
            args.append("median_income,median_income")
        elif cols_invalid:
            args.append("bad_column,median_house_value")
        else:
            args.append("median_income,median_house_value")
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0
        if cols_too_few:
            assert caplog.records[-1].message.startswith("At least two column names")
        elif cols_duplicate:
            assert caplog.records[-1].message.startswith("Duplicate column names")
        elif cols_invalid:
            assert caplog.records[-1].message.startswith("Invalid column name")
        else:
            mock_plot.assert_called_once_with(
                kind="scatter",
                x="median_income",
                y="median_house_value",
                alpha=0.1,
                grid=True,
            )

    def test_invoke2(
        self,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True, housing_csv=True)
        prepare_config_dir(add_config_ini=True)
        mock_plot = mocker.patch("housing_prices.main.scatter_matrix")
        mocker.patch("matplotlib.pyplot.show", return_value=None)
        matplotlib.use("Agg")
        runner = CliRunner()
        args = [
            "scatter-plot",
            "median_house_value,median_income,total_rooms,housing_median_age",
        ]
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0
        mock_plot.assert_called_once_with(
            unittest.mock.ANY,
            figsize=(12, 8),
            grid=True,
        )
