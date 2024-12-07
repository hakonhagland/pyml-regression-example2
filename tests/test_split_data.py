import typing
import pandas as pd
import pytest
from pytest_mock.plugin import MockerFixture

from housing_prices.config import Config
from housing_prices.split_data import SplitStratified
import housing_prices.helpers as helpers
from .common import PrepareConfigDir, PrepareDataDir


class TestSplitStratified:
    @pytest.mark.parametrize(
        "file_exists,bad_columns,bad_rows",
        [
            [False, False, False],
            [True, False, False],
            [True, True, False],
            [True, False, True],
        ],
    )
    def test_split_stratified(
        self,
        file_exists: bool,
        bad_columns: bool,
        bad_rows: bool,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        prepare_config_dir(add_config_ini=True)
        prepare_data_dir(datafiles_exists=True, stratified_dir=True, housing_csv=True)
        config = Config()
        housing = helpers.get_housing_data(config, download=False)
        housing = typing.cast(pd.DataFrame, housing)
        test_ratio = 0.2
        stratify_column = "median_income"
        if not file_exists:
            fn = config.get_stratified_column_csv_filename(stratify_column)
            fn.unlink(missing_ok=True)
        if bad_columns:
            df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
            mocker.patch("pandas.read_csv", return_value=df)
        if bad_rows:
            df = pd.DataFrame({"col1": [1, 2, 3]})
            mocker.patch("pandas.read_csv", return_value=df)
        if file_exists and not (bad_columns or bad_rows):
            SplitStratified(housing, config).split_data(test_ratio, stratify_column)
            assert True
        else:
            with pytest.raises(ValueError) as excinfo:
                SplitStratified(housing, config).split_data(test_ratio, stratify_column)
            if bad_columns:
                assert "has more than one column" in str(excinfo.value)
            elif bad_rows:
                assert "column lengths do not match" in str(excinfo.value)
            elif not file_exists:
                assert "not found" in str(excinfo.value)
