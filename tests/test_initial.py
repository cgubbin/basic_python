"""An example test suite."""

import pytest


class Fruit:
    """A basic class defining a Fruit."""

    def __init__(self, name: str) -> None:
        """Creates a Fruit from it's name."""
        self.name = name

    def __eq__(self, other: str) -> bool:
        """Returns true if self is the same variety as other."""
        return self.name == other.name


@pytest.fixture
def my_fruit() -> Fruit:
    """Creates a Fruit of type `apple`."""
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit: Fruit) -> [Fruit]:
    """Creates a List of Fruit, containing one `banana` and one `my_fruit`."""
    return [Fruit("banana"), my_fruit]


def test_my_fruit_in_basket(my_fruit: Fruit, fruit_basket: [Fruit]) -> None:
    """Exits with code 0 if `my_fruit` is in `fruit_basket`."""
    assert my_fruit in fruit_basket, f"{my_fruit} not found in basket"
