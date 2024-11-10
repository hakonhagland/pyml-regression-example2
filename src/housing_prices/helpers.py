import logging
import requests
import shutil
import tarfile

import pandas as pd
from pathlib import Path
from housing_prices.config import Config
from housing_prices.constants import FileNames


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

    with tarfile.open(tgz_path, "r:gz") as tar:
        tar.extract(extract_file, path=dir_name, filter=filter_tarinfo)
    # move the file to the correct location
    if len(Path(extract_file).parts) > 1:
        extracted_file = dir_name / extract_file
        extracted_file.rename(dir_name / Path(extract_file).name)
        # delete the original directory
        shutil.rmtree(dir_name / Path(extract_file).parts[0])
    logging.info(f"Extracted {extract_file} from {tgz_path}")


def get_housing_data(config: Config, download: bool = True) -> pd.DataFrame | None:
    """Return the data from the CSV file as a pandas DataFrame."""
    data_file = get_housing_local_path(config)
    datadir = config.get_data_dir()
    # Check that the data file exists, if not download it
    if not data_file.exists():
        if download:
            logging.info(f"Data file {data_file} not found. Downloading data ...")
            download_data(datadir)
        else:
            return None
    return pd.read_csv(data_file)


def get_housing_local_path(config: Config) -> Path:
    datadir = config.get_data_dir()
    data_file = Path(datadir) / FileNames.housing_csv
    return data_file
