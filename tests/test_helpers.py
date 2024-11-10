import pytest
from pytest_mock.plugin import MockerFixture

from housing_prices.config import Config
from housing_prices.constants import FileNames
import housing_prices.helpers as helpers
from .common import PrepareConfigDir, PrepareDataDir


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
            filename = "/tmp/test_tar/etc/testfile.txt"
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
