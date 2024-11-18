from rest_framework.exceptions import ValidationError

from settings.validation.account_settings import USERNAME_REGEX
from utils.interfaces.validator import Validator


class UsernameValidator(Validator):
    def validate(self, username: str):
        """
        Validate the provided username based on presence and regex pattern.

        :raises ValidationError: If the username cannot be validated.
        """
        self._validate_presence(username)
        self._validate_pattern(username)

    @staticmethod
    def _validate_presence(username: str):
        """
        Ensure that the username is not None or empty.

        :raises ValidationError: If the username is empty.
        """
        if not username:
            raise ValidationError({"username": "Username cannot be empty."})

    @staticmethod
    def _validate_pattern(username: str) -> None:
        """
        Validates that the provided username matches the required pattern.

        :param username: The username to validate.
        :raises ValidationError: If the username does not meet the pattern requirements.
        """
        if not USERNAME_REGEX.match(username):
            raise ValidationError({"username": "Invalid username."})
