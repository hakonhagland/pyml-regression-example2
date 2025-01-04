import logging
import requests
import shutil
import tarfile
import zlib

import sklearn  # type: ignore

import numpy as np
import pandas as pd
from pathlib import Path

import sklearn.impute  # type: ignore
import sklearn.preprocessing  # type: ignore
from housing_prices.config import Config
from housing_prices.constants import FileNames, ImputerStrategy


def apply_imputer(data: pd.DataFrame, strategy: ImputerStrategy) -> pd.DataFrame:
    """Impute missing values in the DataFrame using the specified strategy."""

    # Only consider numeric columns, i.e. skip the ocean_proximity column
    numeric_data = data.select_dtypes(include=[np.number])
    imputer = sklearn.impute.SimpleImputer(strategy=strategy.value)
    imputer.fit(numeric_data)
    # NOTE: Since the imputer.transform() method returns a numpy array, we need to
    #       convert it back to a DataFrame with the original column names and index
    logging.info(f"Imputing missing values using strategy: {strategy.value}")
    logging.info(f"Imputing on columns: {numeric_data.columns}")
    logging.info(f"Imputer statistics: {imputer.statistics_}")
    return pd.DataFrame(
        imputer.transform(numeric_data),
        columns=numeric_data.columns,
        index=numeric_data.index,
    )


def download_data(datadir: Path) -> None:
    """Download data files from various URLs."""
    download_items = []
    filename1 = FileNames.housing_tgz
    data_url1 = f"https://github.com/ageron/data/raw/main/{filename1}"
    download_items.append((filename1, data_url1))
    download_data_from_url(datadir, download_items=download_items)
    extract_file_from_tgz(
        dir_name=datadir,
        tgz_file=filename1,
        extract_file=f"housing/{FileNames.housing_csv}",
    )
    (datadir / filename1).unlink()  # Delete the tgz file after extracting
    # logging.info(f"Data files downloaded and extracted to {datadir}")


def download_file(savename: Path, data_url: str) -> None:
    response = requests.get(data_url)
    response.raise_for_status()  # Ensure we notice bad responses
    logging.info(f"Ensure the directory {savename.parent} exists")
    savename.parent.mkdir(parents=True, exist_ok=True)
    logging.info(f"Opening file {savename} for writing")
    # NOTE: Using 'wb' should work for all file types.
    with open(savename, "wb") as f:
        f.write(response.content)
    logging.info(f"Data downloaded and saved to {savename}")


def download_data_from_url(
    datadir: Path, download_items: list[tuple[str, str]]
) -> None:
    for filename, data_url in download_items:
        savename = Path(datadir) / filename
        if savename.exists():
            logging.info(f"Data file {savename} already exists, skipping download")
            continue
        download_file(savename, data_url)


def extract_file_from_tgz(dir_name: Path, tgz_file: str, extract_file: str) -> None:
    """Extract a file from a tgz archive. Assume the .tgz file is located in ``dir_name`` and
    save the extracted file in the same ``dir_name``. The ``extract_file```should be a
    relative path within the tgz file"""
    if not (dir_name / tgz_file).exists():
        raise FileNotFoundError(f"File not found: {dir_name / tgz_file}")
    if Path(extract_file).is_absolute():
        raise ValueError("extract_file should be a relative path")
    tgz_path = dir_name / tgz_file

    def filter_tarinfo(
        tarinfo: tarfile.TarInfo, destination: str
    ) -> tarfile.TarInfo | None:
        # Allow extraction only if the file path is within the base directory
        target_path = Path(destination) / tarinfo.name
        if target_path.resolve().is_relative_to(Path(destination).resolve()):
            return tarinfo
        else:  # pragma: no cover
            logging.warning(f"Skipping potentially unsafe path: {tarinfo.name}")
            return None

    # NOTE: On Windows, the tarfile.extract() method does not overwrite existing files
    #   so this may fail with a FileExistsError if the file exists on Windows
    with tarfile.open(tgz_path, "r:gz") as tar:
        tar.extract(extract_file, path=dir_name, filter=filter_tarinfo)
    # move the file to the correct location
    if len(Path(extract_file).parts) > 1:
        extracted_file = dir_name / extract_file
        extracted_file.rename(dir_name / Path(extract_file).name)
        # delete the original directory
        shutil.rmtree(dir_name / Path(extract_file).parts[0])
    logging.info(f"Extracted {extract_file} from {tgz_path}")


def get_extra_col_name_info(column_name: str) -> str:
    info = ""
    if column_name == "median_income":
        info = "($) (capped at 15, and scaled by 10,000)"
    return info


def get_housing_data(config: Config, download: bool = True) -> pd.DataFrame | None:
    """Return the data from the CSV file as a pandas DataFrame."""
    data_file = config.get_housing_local_path()
    datadir = config.get_data_dir()
    # Check that the data file exists, if not download it
    if not data_file.exists():
        if download:
            logging.info(f"Data file {data_file} not found. Downloading data ...")
            download_data(datadir)
        else:
            return None
    return pd.read_csv(data_file)


def one_hot_encode(data: pd.DataFrame) -> pd.DataFrame:
    """One-hot encode the data in the specified column."""
    encoder = sklearn.preprocessing.OneHotEncoder()
    encoded_data = encoder.fit_transform(data)
    # Convert to DataFrame and set the column names
    return pd.DataFrame(
        encoded_data.toarray(),
        columns=encoder.get_feature_names_out(data.columns),
        index=data.index,
    )


def read_stratified_column_bins(config: Config, column_name: str) -> list[float]:
    bin_file = config.get_stratified_column_bin_filename(column_name)
    if not bin_file.exists():
        raise FileNotFoundError(f"Bin file {str(bin_file)} not found")
    with open(bin_file, "r") as f:
        bins = [float(line.strip()) for line in f]
    return bins


def save_imputed_data(
    config: Config, data: pd.DataFrame, strategy: ImputerStrategy
) -> None:
    imputed_file = config.get_imputed_data_csv_filename(strategy.value)
    data.to_csv(imputed_file, index=False)
    logging.info(f"Imputed data saved to {imputed_file}")


def save_one_hot_encoded_data(
    config: Config, data: pd.DataFrame, column_name: str
) -> None:
    encoded_file = config.get_one_hot_encoded_csv_filename(column_name)
    data.to_csv(encoded_file, index=False)
    logging.info(f"One-hot encoded data saved to {encoded_file}")


def save_stratified_column(
    config: Config,
    column_name: str,
    stratified: pd.Series,  # type: ignore
    bins: list[float],
) -> None:
    stratified_file = config.get_stratified_column_csv_filename(column_name)
    stratified.to_csv(stratified_file, index=False)
    bin_file = config.get_stratified_column_bin_filename(column_name)
    with open(bin_file, "w") as f:
        f.write("\n".join([str(b) for b in bins]))
    logging.info(f"Stratified column saved to {stratified_file}")
    logging.info(f"Bin info saved to {bin_file}")


def split_data_with_id_hash(
    data: pd.DataFrame, test_ratio: float, id_column: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    ids = data[id_column]

    def is_id_in_test_set(identifier: int, test_ratio: float) -> bool:
        # NOTE: On macOS and on Linux: zlib.crc32(np.int64(identifier)) works..
        #       but on Windows, mypy requires the bytes version below instead
        identifier_bytes = np.int64(identifier).tobytes()
        return zlib.crc32(identifier_bytes) < test_ratio * 2**32

    in_test_set = ids.apply(lambda id_: is_id_in_test_set(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]
