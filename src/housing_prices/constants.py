import enum


class Directories:
    columns = "columns"
    crc = "crc"
    imputed = "imputed"
    one_hot = "one_hot"
    rbf = "rbf"
    scaled = "scaled"
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


class BaseEnum(enum.Enum):
    """Base class for enums with keys and values."""

    @classmethod
    def keys(cls) -> set[str]:
        return set(cls.__members__.keys())

    @classmethod
    def values(cls) -> set[str]:
        return {member.value for member in cls}


class ImputerStrategy(BaseEnum):
    """Imputation strategies."""

    MEAN = "mean"
    MEDIAN = "median"
    MOST_FREQUENT = "most_frequent"


class ScalingMethod(BaseEnum):
    """Scaling methods for the data."""

    STANDARD = "standard"
    MINMAX = "minmax"


class TestSetGenMethod(BaseEnum):
    """Test set generation methods."""

    CRC = "CRC"  # Cyclic redundancy check
    RANDOM = "RND"
    STRATIFIED = "STR"

    @property
    def dirname(self) -> str:  # For creating directories with lowercase names
        return self.name.lower()
