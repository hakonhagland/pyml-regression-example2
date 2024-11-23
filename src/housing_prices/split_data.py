import logging
import pandas as pd


from housing_prices.config import Config
from housing_prices import helpers


class SplitCrc:
    def __init__(self, data: pd.DataFrame, config: Config):
        self.data = data
        self.config = config

    def split_data(self, test_ratio: float) -> None:
        data = self.data.reset_index()
        train_set, test_set = helpers.split_data_with_id_hash(data, test_ratio, "index")
        datadir = self.config.get_data_dir()
        train_file = helpers.get_train_set_path(datadir, "crc")
        train_set.to_csv(train_file, index=False)
        logging.info(f"Training data saved to {train_file}")
        test_file = helpers.get_test_set_path(datadir, "crc")
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
