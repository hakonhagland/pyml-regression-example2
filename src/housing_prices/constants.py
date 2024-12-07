import enum


class Directories:
    columns = "columns"
    crc = "crc"
    stratified = "stratified"


class FileNames:
    bins_txt = "bins.txt"
    column_csv = "column.csv"
    housing_tgz = "housing.tgz"
    housing_csv = "housing.csv"
    test_csv = "test.csv"
    tgz_test_file1 = "absolute_path_test.tgz"
    tgz_test_file2 = "mixed_path_test.tgz"
    train_csv = "train.csv"


class TestSetGenMethod(enum.Enum):
    """Test set generation methods."""

    CRC = "CRC"  # Cyclic redundancy check
    RANDOM = "RND"
    STRATIFIED = "STR"

    @property
    def dirname(self) -> str:  # For creating directories with lowercase names
        return self.name.lower()

    @staticmethod
    def keys() -> set[str]:
        return set(TestSetGenMethod.__members__.keys())

    @staticmethod
    def values() -> set[str]:
        return {member.value for member in TestSetGenMethod}
