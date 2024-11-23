import enum


class FileNames:
    housing_tgz = "housing.tgz"
    housing_csv = "housing.csv"
    tgz_test_file1 = "absolute_path_test.tgz"
    tgz_test_file2 = "mixed_path_test.tgz"


class TestSetGenMethod(enum.Enum):
    """Test set generation methods."""

    CRC = "CRC"  # Cyclic redundancy check
    RANDOM = "RND"
    STRATIFIED = "STR"

    @staticmethod
    def keys() -> set[str]:
        return set(TestSetGenMethod.__members__.keys())

    @staticmethod
    def values() -> set[str]:
        return {member.value for member in TestSetGenMethod}
