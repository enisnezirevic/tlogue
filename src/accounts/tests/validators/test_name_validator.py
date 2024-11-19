import pytest
from rest_framework.exceptions import ValidationError

from accounts.validators.name_validator import NameValidator


def name_validator():
    return NameValidator("first_name")


@pytest.mark.parametrize("name", [""])
def test_validation_first_name_is_empty_should_raise_error(name):
    with pytest.raises(ValidationError):
        name_validator().validate(name)


@pytest.mark.parametrize(
    "name, is_valid",
    [
        # Valid names
        ("John", True),
        ("Renée", True),
        ("François", True),
        ("Jean-Pierre", True),
        ("O'Neil", True),
        ("Jürgen", True),
        ("José", True),
        ("María", True),
        ("Zoë", True),
        ("Mário", True),
        ("Álvaro", True),
        ("Javier", True),
        ("Vladimir", True),

        # Invalid names
        ("李", False),
        ("Ant!", False),
        ("Ahmed123", False),
        ("John李", False),
        ("Annaअ", False),
        ("👑", False),
        ("😊John", False),
        ("John😊", False),
        ("Anna_123", False),
        ("Jane^Doe", False),
        ("Sarah-Jane!!!", False),
        ("Дмитрий", False),
        ("Иван", False),
    ],
)
def test_validation_name_matches_the_regex_should_pass(name, is_valid):
    try:
        name_validator().validate(name)
        assert is_valid, f"Expected {name} to be invalid but it was valid."
    except ValidationError:
        assert not is_valid, f"Expected {name} to be valid but it was invalid."
