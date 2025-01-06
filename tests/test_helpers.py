import os
import pytest

import pandas as pd

from pytest_mock.plugin import MockerFixture

from housing_prices.config import Config
from housing_prices.constants import FileNames, ScalingMethod
import housing_prices.helpers as helpers
from .common import PrepareConfigDir, PrepareDataDir


class TestStratifiedColumnBins:
    @pytest.mark.parametrize("file_exists", [False, True])
    def test_read_stratified_column_bins(
        self,
        file_exists: bool,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        prepare_config_dir(add_config_ini=True)
        prepare_data_dir(datafiles_exists=True, stratified_dir=True)
        config = Config()
        bin_file = config.get_stratified_column_bin_filename("median_income")
        if not file_exists:
            # Remove the file
            bin_file.unlink(missing_ok=True)
        column_name = "median_income"
        if file_exists:
            bins = helpers.read_stratified_column_bins(config, column_name)
            assert len(bins) == 6
        else:
            with pytest.raises(FileNotFoundError):
                helpers.read_stratified_column_bins(config, column_name)


class TestDownloadData:
    def test_download_from_url(
        self,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        prepare_config_dir(add_config_ini=True)
        prepare_data_dir(datafiles_exists=True)
        config = Config()
        filename = FileNames.housing_tgz
        download_items = [(filename, "dummy_url")]
        datadir = config.get_data_dir()
        helpers.download_data_from_url(datadir, download_items=download_items)
        assert True

    @pytest.mark.parametrize("tgz_exists", [False, True])
    def test_extract_file_from_tgz_fail(
        self,
        tgz_exists: bool,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        prepare_config_dir(add_config_ini=True)
        prepare_data_dir(datafiles_exists=True)
        config = Config()
        if tgz_exists:
            tgz_file = FileNames.tgz_test_file1
            filename = os.path.join("tmp", "test_tar", "etc", "testfile.txt")
            filename = os.path.abspath(filename)
        else:
            tgz_file = "non_existent.tgz"
            filename = "dummy_file"
        datadir = config.get_data_dir()
        if tgz_exists:
            with pytest.raises(ValueError):
                helpers.extract_file_from_tgz(
                    datadir, tgz_file=tgz_file, extract_file=filename
                )
        else:
            with pytest.raises(FileNotFoundError):
                helpers.extract_file_from_tgz(
                    datadir, tgz_file=tgz_file, extract_file=filename
                )
        assert True

    def test_extract_file_from_tgz(
        self,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        prepare_config_dir(add_config_ini=True)
        prepare_data_dir(datafiles_exists=True)
        config = Config()
        tgz_file = FileNames.tgz_test_file2
        filename = "etc/relative_testfile.txt"
        datadir = config.get_data_dir()
        helpers.extract_file_from_tgz(datadir, tgz_file=tgz_file, extract_file=filename)
        assert True

    def test_get_housing_data_fail(
        self,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        prepare_config_dir(add_config_ini=True)
        prepare_data_dir(datafiles_exists=False)
        config = Config()
        helpers.get_housing_data(config, download=False)
        assert True


class TestScalingMethod:
    def test_scale_data(self) -> None:
        data = pd.DataFrame([[1, 2], [3, 4]], columns=["A", "B"])
        scaled_data = helpers.scale_data(data, ScalingMethod.STANDARD)
        assert scaled_data.shape == (2, 2)
        assert scaled_data.loc[0, "A"] == -1
        assert scaled_data.loc[0, "B"] == -1
        assert scaled_data.loc[1, "A"] == 1
        assert scaled_data.loc[1, "B"] == 1
        scaled_data = helpers.scale_data(data, ScalingMethod.MINMAX)
        assert scaled_data.loc[0, "A"] == 0
        assert scaled_data.loc[0, "B"] == 0
        assert scaled_data.loc[1, "A"] == 1
        assert scaled_data.loc[1, "B"] == 1
