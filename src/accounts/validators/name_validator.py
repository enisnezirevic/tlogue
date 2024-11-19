from rest_framework.exceptions import ValidationError

from settings.validation.account_settings import NAME_REGEX
from utils.interfaces.validator import Validator


class NameValidator(Validator):
    def __init__(self, name_prefix: str):
        """
        Class used to validate the name of a user.

        :param name_prefix: The prefix to be used for error messages. Should be either 'first_name' or 'last_name'.
        """
        self.name_prefix = name_prefix

    def validate(self, name: str) -> None:
        """
        Validates the provided name based on presence, and regex pattern.

        :param name: name to validate.
        :raises ValidationError: Raised if name cannot be validated.
        """
        self.__validate_presence(name)
        self.__validate_pattern(name)

    def __validate_presence(self, name: str) -> None:
        """
        Ensures that the name is not empty or None.

        :param name: name to validate.
        :raises ValidationError: Raised if name cannot be validated.
        """
        if not isinstance(name, str) or not name:
            raise ValidationError({f"{self.name_prefix}": "Cannot be empty."})

    def __validate_pattern(self, name: str) -> None:
        """
        Validates that the provided name matches the required pattern.

        :param name: name to validate.
        :raises ValidationError: Raised if name cannot be validated.
        """
        if not NAME_REGEX.match(name):
            raise ValidationError({
                f"{self.name_prefix}": "Must only contain alphabetic characters from the Latin alphabet."
            })
