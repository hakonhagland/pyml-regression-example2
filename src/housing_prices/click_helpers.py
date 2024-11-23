from housing_prices.constants import TestSetGenMethod
from typing import Union
import click


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
