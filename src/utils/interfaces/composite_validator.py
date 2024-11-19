from utils.interfaces.validator import Validator


class CompositeValidator(Validator):
    """A validator that aggregates multiple validators and applies them in sequence."""

    def __init__(self, validators: list[Validator]):
        """
        Initialize with a list of validators.
        :param validators: A list of Validator instances.
        """
        self.validators = validators

    def validate(self, value: any):
        """
        Apply all validators to the given value.
        :param value: The value to validate.
        :raises Exception: If any validator raises an exception.
        """
        for validator in self.validators:
            validator.validate(value)
