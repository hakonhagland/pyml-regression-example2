import configparser
import importlib.resources  # access non-code resources
import logging
from configparser import ConfigParser
from pathlib import Path

import platformdirs

from housing_prices.constants import Directories, TestSetGenMethod, FileNames
from housing_prices.exceptions import ConfigException


class Config:
    # NOTE: This is made a class variable since it must be accessible from
    #   pytest before creating an object of this class
    config_fn = "config.ini"
    dirlock_fn = ".dirlock"

    def __init__(self) -> None:
        self.appname = "pyml_housing_prices"
        self.lockfile_string = f"author=HH, appname={self.appname}"
        self.config_dir = self.check_config_dir()
        self.config_path = Path(self.config_dir) / self.config_fn
        self.read_config()
        self.datadir_path = self.get_data_dir_path()

    def check_config_dir(self) -> Path:
        config_dir = platformdirs.user_config_dir(appname=self.appname)
        path = Path(config_dir)
        lock_file = path / self.dirlock_fn
        if path.exists():
            if path.is_file():
                raise ConfigException(
                    f"Config directory {str(path)} is a file. Expected directory"
                )
            self.check_correct_config_dir(lock_file)
        else:
            path.mkdir(parents=True)
            with open(str(lock_file), "a", encoding="utf_8") as fp:
                fp.write(self.lockfile_string)
        return path

    def check_correct_config_dir(self, lock_file: Path) -> None:
        """The config dir might be owned by another app with the same name"""
        if lock_file.exists():
            if lock_file.is_file():
                with open(str(lock_file), encoding="utf_8") as fp:
                    line = fp.readline()
                    if line.startswith(self.lockfile_string):
                        return
                msg = "bad content"
            else:
                msg = "is a directory"
        else:
            msg = "missing"
        raise ConfigException(
            f"Unexpected: Config dir lock file: {msg}. "
            f"The data directory {str(lock_file.parent)} might be owned by another app."
        )

    def check_correct_data_dir(self, lock_file: Path) -> None:
        """The data dir might be owned by another app with the same name"""
        if lock_file.exists():
            if lock_file.is_file():
                with open(str(lock_file), encoding="utf_8") as fp:
                    line = fp.readline()
                    if line.startswith(self.lockfile_string):
                        return
                msg = "bad content"
            else:
                msg = "is a directory"
        else:
            msg = "missing"
        raise ConfigException(
            f"Unexpected: Data dir lock file: {msg}. "
            f"The data directory {str(lock_file.parent)} might be owned by another app."
        )

    def get_cluster_similarities_csv_filename(
        self, num_clusters: int, gamma: float
    ) -> Path:
        datadir: Path = self.get_data_dir()
        dir_ = datadir / Directories.cluster_similarities
        if not dir_.exists():
            dir_.mkdir(parents=True)
        csv_file = dir_ / f"{num_clusters}_{gamma}.csv"
        return csv_file

    def get_config_dir(self) -> Path:
        return self.config_dir  # pragma: no cover

    def get_data_dir(self) -> Path:
        return self.datadir_path  # pragma: no cover

    def get_data_dir_path(self) -> Path:
        data_dir = platformdirs.user_data_dir(appname=self.appname)
        path = Path(data_dir)
        lock_file = path / self.dirlock_fn
        if path.exists():
            if path.is_file():
                raise ConfigException(
                    f"Data directory {str(path)} is a file. Expected directory"
                )
            self.check_correct_data_dir(lock_file)
        else:
            path.mkdir(parents=True)
            with open(str(lock_file), "a", encoding="utf_8") as fp:
                fp.write(self.lockfile_string)
        return path

    def get_config_path(self) -> Path:
        return self.config_path

    def get_housing_local_path(self) -> Path:
        datadir = self.get_data_dir()
        data_file = Path(datadir) / FileNames.housing_csv
        return data_file

    def get_imputed_data_csv_filename(self, strategy: str) -> Path:
        datadir: Path = self.get_data_dir()
        dir_ = datadir / Directories.imputed
        if not dir_.exists():
            dir_.mkdir(parents=True)
        csv_file = dir_ / f"{strategy}.csv"
        return csv_file

    def get_one_hot_encoded_csv_filename(self, column_name: str) -> Path:
        datadir: Path = self.get_data_dir()
        dir_ = datadir / Directories.one_hot
        if not dir_.exists():
            dir_.mkdir(parents=True)
        csv_file = dir_ / f"{column_name}.csv"
        return csv_file

    def get_rbf_kernel_csv_filename(
        self, column_name: str, peak_value: float, gamma: float
    ) -> Path:
        datadir: Path = self.get_data_dir()
        dir_ = datadir / Directories.rbf
        if not dir_.exists():
            dir_.mkdir(parents=True)
        csv_file = dir_ / f"{column_name}_{peak_value}_{gamma}.csv"
        return csv_file

    def get_scaled_data_csv_filename(self, strategy: str) -> Path:
        datadir: Path = self.get_data_dir()
        dir_ = datadir / Directories.scaled
        if not dir_.exists():
            dir_.mkdir(parents=True)
        csv_file = dir_ / f"{strategy}.csv"
        return csv_file

    def get_stratified_column_csv_filename(self, column_name: str) -> Path:
        dir_ = self.get_stratified_column_dir(column_name)
        csv_file = dir_ / FileNames.column_csv
        return csv_file

    def get_stratified_column_bin_filename(self, column_name: str) -> Path:
        dir_ = self.get_stratified_column_dir(column_name)
        filename = dir_ / FileNames.bins_txt
        return filename

    def get_stratified_column_dir(self, column_name: str) -> Path:
        datadir: Path = self.get_data_dir()
        strat_dir = TestSetGenMethod.STRATIFIED.dirname
        dir_ = datadir / strat_dir / Directories.columns / f"{column_name}"
        if not dir_.exists():
            dir_.mkdir(parents=True)
        return dir_

    def get_test_train_dir(
        self, splitting_method: TestSetGenMethod, ensure_exists: bool = True
    ) -> Path:
        datadir = self.get_data_dir()
        dir_ = datadir / splitting_method.dirname
        if ensure_exists:
            dir_.mkdir(parents=True, exist_ok=True)
        return dir_

    def get_train_set_path(self, splitting_method: TestSetGenMethod) -> Path:
        dir_ = self.get_test_train_dir(splitting_method)
        return dir_ / FileNames.train_csv

    def get_test_set_path(self, splitting_method: TestSetGenMethod) -> Path:
        dir_ = self.get_test_train_dir(splitting_method)
        return dir_ / FileNames.test_csv

    def read_config(self) -> None:
        path = self.get_config_path()
        if path.exists():
            if not path.is_file():
                raise ConfigException(
                    f"Config filename {str(path)} exists, but filetype is not file"
                )
        else:
            with open(str(self.get_config_path()), "w", encoding="utf_8") as _:
                pass  # only create empty file
        config = configparser.ConfigParser()
        self.read_defaults(config)
        config.read(str(path))
        logging.info(f"Read config file: {str(path)}")
        self.config = config

    def read_defaults(self, config: ConfigParser) -> None:
        path = importlib.resources.files("housing_prices.data").joinpath(
            "default_config.ini"
        )
        config.read(str(path))
