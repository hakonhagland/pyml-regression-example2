from housing_prices.constants import TestSetGenMethod
from typing import Union
import click


def validate_bins(
    ctx: click.Context, param: Union[click.Option, click.Parameter], value: str
) -> list[float]:
    try:
        bins = [float(b) for b in value.split(",")]
        if not all(earlier < later for earlier, later in zip(bins, bins[1:])):
            raise click.BadParameter(f"Bins must be in ascending order. Got: {value}")
        return bins
    except ValueError:
        raise click.BadParameter(
            f"Invalid bin value '{value}'. Must be a comma-separated list of numbers."
        )


def validate_column_names(
    ctx: click.Context, param: Union[click.Option, click.Parameter], value: str
) -> list[str]:
    return value.split(",")


def validate_test_set_gen_method(
    ctx: click.Context, param: Union[click.Option, click.Parameter], value: str
) -> TestSetGenMethod:
    value = value.upper()
    if value in TestSetGenMethod.keys():
        return TestSetGenMethod[value]
    try:
        return TestSetGenMethod(value)
    except ValueError:
        values = ", ".join(list(TestSetGenMethod.values()))
        keys = ", ".join(list(TestSetGenMethod.keys()))
        raise click.BadParameter(
            f"Invalid test set generation method value '{value}'. Must be one of: {values}. "
            f"Or alternatively, use the full names: {keys}."
        )
