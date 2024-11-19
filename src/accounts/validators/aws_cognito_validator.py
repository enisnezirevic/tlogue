from rest_framework.exceptions import ValidationError

from accounts.models import SignUpUserModel
from accounts.services.aws_cognito_identity_provider import AwsCognitoIdentityProvider
from utils.interfaces.validator import Validator


class AwsCognitoValidator(Validator):
    """
    Validator that makes external API calls to AWS Cognito services for validation.
    """

    def __init__(self, identity_provider: AwsCognitoIdentityProvider):
        """
        Initialize the validator with the identity provider.

        :param identity_provider: Service for interacting with AWS Cognito.
        """
        self.identity_provider = identity_provider

    def __validate_username_availability(self, username: str):
        """
        Validate that the username is not already taken in AWS Cognito.

        :param username: The username to check.
        :raises ValidationError: If the username is already in use.
        """
        if self.identity_provider.is_preferred_username_taken(username):
            raise ValidationError({"message": "Username is already in use."})

    def validate(self, user: SignUpUserModel):
        """
        Perform validations using AWS Cognito services.

        :param user: An object containing user attributes to validate.
        :raises ValidationError: If validation fails.
        """
        self.__validate_username_availability(user.username)
