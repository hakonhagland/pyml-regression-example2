# import logging
import shutil
from pathlib import Path
from unittest.mock import Mock
# import typing

import pytest
from pytest_mock.plugin import MockerFixture

from housing_prices.config import Config
from housing_prices.constants import FileNames
from .common import DataFileContents, PrepareConfigDir, PrepareDataDir, MockRequestGet

PytestDataDict = dict[str, str]


@pytest.fixture(scope="session")
def test_file_path() -> Path:
    return Path(__file__).parent / "files"


@pytest.fixture(scope="session")
def test_data() -> PytestDataDict:
    return {
        "config_dir": "config",
        "data_dir": "data",
    }


# @pytest.fixture()
# def config_oject(
#     data_dir_path: Path,
#     prepare_config_dir: PrepareConfigDir,
#     mocker: MockerFixture,
# ) -> Config:
#     data_dir = data_dir_path
#     config_dir = prepare_config_dir(add_config_ini=True)
#     mocker.patch(
#         "platformdirs.user_config_dir",
#         return_value=config_dir,
#     )
#     data_dir = data_dir_path
#     mocker.patch(
#         "platformdirs.user_data_dir",
#         return_value=data_dir,
#     )
#     return Config()


@pytest.fixture()
def config_dir_path(prepare_config_dir: PrepareConfigDir) -> Path:
    return prepare_config_dir(add_config_ini=False)


@pytest.fixture()
def data_dir_path(prepare_data_dir: PrepareDataDir) -> Path:
    return prepare_data_dir(datafiles_exists=True)


@pytest.fixture()
def mock_requests_get(mocker: MockerFixture) -> MockRequestGet:
    def _mock_requests_get(datafile_contents: bytes) -> Mock:
        mock_response: Mock = mocker.Mock()
        mock_response.content = datafile_contents
        mock_response.raise_for_status = mocker.Mock()
        # Patch requests.get to return the mock response
        mocker.patch("requests.get", return_value=mock_response)
        return mock_response

    return _mock_requests_get


@pytest.fixture()
def prepare_config_dir(
    tmp_path: Path,
    test_file_path: Path,
    test_data: PytestDataDict,
    mocker: MockerFixture,
) -> PrepareConfigDir:
    def _prepare_config_dir(add_config_ini: bool) -> Path:
        config_dir = tmp_path / test_data["config_dir"]
        config_dir.mkdir()
        config_dirlock_fn = test_file_path / test_data["config_dir"] / Config.dirlock_fn
        mocker.patch(
            "platformdirs.user_config_dir",
            return_value=config_dir,
        )
        shutil.copy(config_dirlock_fn, config_dir)
        # if add_config_ini:
        #     config_ini_fn = test_file_path / test_data["config_dir"] / Config.config_fn
        #     save_fn = config_dir / config_ini_fn.name
        #     shutil.copy(config_ini_fn, save_fn)
        return config_dir

    return _prepare_config_dir


@pytest.fixture()
def prepare_data_dir(
    tmp_path: Path,
    test_file_path: Path,
    test_data: PytestDataDict,
    mocker: MockerFixture,
) -> PrepareDataDir:
    def _prepare_data_dir(datafiles_exists: bool, housing_csv: bool = False) -> Path:
        data_dir = tmp_path / test_data["data_dir"]
        data_dir.mkdir()
        data_dirlock_fn = test_file_path / test_data["data_dir"] / Config.dirlock_fn
        shutil.copy(data_dirlock_fn, data_dir)
        mocker.patch(
            "platformdirs.user_data_dir",
            return_value=data_dir,
        )
        if datafiles_exists:
            filenames = [
                FileNames.housing_tgz,
                FileNames.tgz_test_file1,
                FileNames.tgz_test_file2,
            ]
            if housing_csv:
                filenames.append(FileNames.housing_csv)  # pragma: no cover
            for filename in filenames:
                datafile_fn = test_file_path / test_data["data_dir"] / filename
                shutil.copy(datafile_fn, data_dir)
        return data_dir

    return _prepare_data_dir


@pytest.fixture()
def datafile_contents(
    test_file_path: Path, test_data: PytestDataDict
) -> DataFileContents:
    def _datafile_contents(filename: str) -> bytes:
        datafile_fn = test_file_path / test_data["data_dir"] / filename
        with open(datafile_fn, "rb") as fp:
            return fp.read()

    return _datafile_contents
