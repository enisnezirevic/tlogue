import pytest
from rest_framework.exceptions import ValidationError

from accounts.validators.username_validator import UsernameValidator


def username_validator():
    return UsernameValidator()


@pytest.mark.parametrize("username", [None])
def test_validation_username_is_null_should_fail(username):
    with pytest.raises(ValidationError):
        username_validator().validate(username)


@pytest.mark.parametrize("username", ["#&&*#$"])
def test_validation_username_contains_special_characters_should_raise_error(username):
    with pytest.raises(ValidationError):
        username_validator().validate(username)


@pytest.mark.parametrize("username", ["Tx"])
def test_validation_username_is_below_minimum_length_should_raise_error(username):
    with pytest.raises(ValidationError):
        username_validator().validate(username)


@pytest.mark.parametrize("username", ["Username123456789101112"])
def test_validation_username_is_beyond_maximum_length_should_raise_error(username):
    with pytest.raises(ValidationError):
        username_validator().validate(username)


@pytest.mark.parametrize("username, is_valid", [
    ("Username123", True),# starts with a letter, contains no consecutive underscores, within 3-15 chars
    ("User_name", True),  # underscore allowed but not consecutive or at the start/end
    ("User123", True),  # only letters and numbers
    ("Us3r_123", True),  # letters, numbers, single underscore
    ("User__Name", False),  # contains consecutive underscores
    ("_UserName", False),  # starts with an underscore
    ("UserName_", False),  # ends with an underscore
    ("__Username", False),  # starts with consecutive underscores
    ("Username123456789101112", False),  # too long, exceeds 15 characters
])
def test_validation_username_matches_regex(username, is_valid):
    try:
        username_validator().validate(username)
        assert is_valid, f"Expected {username} to be a valid username."
    except ValidationError:
        assert not is_valid, f"Expected {username} to be valid, but it was not."
