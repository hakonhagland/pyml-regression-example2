import logging
import pandas as pd
from sklearn import model_selection  # type: ignore

from housing_prices.config import Config
from housing_prices.constants import TestSetGenMethod
from housing_prices import helpers


def save_split_data(
    config: Config,
    data: pd.DataFrame,
    train_set: pd.DataFrame,
    test_set: pd.DataFrame,
    method: TestSetGenMethod,
) -> None:
    train_file = config.get_train_set_path(method)
    train_set.to_csv(train_file, index=False)
    logging.info(f"Training data saved to {train_file}")
    test_file = config.get_test_set_path(method)
    test_set.to_csv(test_file, index=False)
    logging.info(f"Test data saved to {test_file}")
    orig_size = len(data)
    train_size = len(train_set)
    test_size = len(test_set)
    logging.info(
        f"Original data size: {orig_size}, Train set size: {train_size}, Test set size: {test_size}"
    )
    test_ratio_computed = test_size / orig_size
    logging.info(f"Computed test ratio: {test_ratio_computed}")


class SplitCrc:
    def __init__(self, data: pd.DataFrame, config: Config):
        self.data = data
        self.config = config

    def split_data(self, test_ratio: float) -> None:
        data = self.data.reset_index()
        train_set, test_set = helpers.split_data_with_id_hash(data, test_ratio, "index")
        save_split_data(self.config, data, train_set, test_set, TestSetGenMethod.CRC)


class SplitStratified:
    def __init__(self, data: pd.DataFrame, config: Config):
        self.data = data
        self.config = config

    def split_data(self, test_ratio: float, column_name: str) -> None:
        fn = self.config.get_stratified_column_csv_filename(column_name)
        if not fn.exists():
            raise ValueError(f"Stratified column file {str(fn)} not found")
        df = pd.read_csv(fn)
        bins = helpers.read_stratified_column_bins(self.config, column_name)
        logging.info(f"Stratified column {column_name} read from {str(fn)}")
        logging.info(f"Bins: {bins}")
        if len(df.columns) != 1:
            raise ValueError(
                f"Stratified column file {str(fn)} has more than one column"
            )
        col_name = df.columns[0]
        # Check that the number of rows in self.data and the length of the stratified column match
        if len(self.data) != len(df):
            raise ValueError(
                f"Data and stratified column lengths do not match: {len(self.data)} != {len(df)}"
            )
        train_set, test_set = model_selection.train_test_split(
            self.data, test_size=test_ratio, stratify=df[col_name], random_state=42
        )
        save_split_data(
            self.config, self.data, train_set, test_set, TestSetGenMethod.STRATIFIED
        )
