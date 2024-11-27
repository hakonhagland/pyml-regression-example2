import logging

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
    @pytest.mark.parametrize("method", ["crc", "random", "rnd", "bad"])
    def test_invoke(
        self,
        method: str,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True, housing_csv=False)
        prepare_config_dir(add_config_ini=True)
        runner = CliRunner()
        args = ["create-test-set", "--test-ratio", "0.2", "--method", method]
        result = runner.invoke(main.main, args)
        if method == "crc":
            assert result.exit_code == 0
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
        bins = "4,5,5.5,6,9"
        if bins_too_narrow:
            bins = "6,16,32"
        elif bins_descending:
            bins = "9,6,5,3"
        elif bins_nan:
            bins = "a,4,5,5.5,6,9,a"
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