import logging

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
    def test_invoke(
        self,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True, housing_csv=False)
        prepare_config_dir(add_config_ini=True)
        runner = CliRunner()
        args = ["describe-column", "total_rooms"]
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0


class TestPlotHistogramsCmd:
    def test_invoke(
        self,
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
        import matplotlib

        matplotlib.use("Agg")

        runner = CliRunner()
        args = ["plot-histograms"]
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0
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
