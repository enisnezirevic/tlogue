import logging

from botocore.exceptions import ClientError
from rest_framework.exceptions import ValidationError

from accounts.services.aws_cognito_client import AwsCognitoClient
from accounts.services.aws_cognito_identity_provider import AwsCognitoIdentityProvider
from accounts.services.user_service import UserService
from accounts.settings.cognito_config import AwsCognitoConfig, DEFAULT_USER_GROUP
from accounts.validators.account_validator import AccountValidator


class UserManagementService:
    def __init__(self):
        self.aws_cognito_client = AwsCognitoClient()
        self.aws_cognito_service = AwsCognitoIdentityProvider(
            cognito_client=self.aws_cognito_client,
            client_id=AwsCognitoConfig.CLIENT_ID,
            client_secret=AwsCognitoConfig.CLIENT_SECRET
        )
        self.user_service = UserService()

    def create_user(self, user):
        # Validation
        account_validator = AccountValidator()
        account_validator.validate(user)

        username_available = self.user_service.is_username_available(user.username)
        if not username_available:
            raise ValidationError({"username": "Username is already in use."})

        email_available = self.user_service.is_email_available(user.email)
        if not email_available:
            raise ValidationError({"email": "This email address is already associated with an existing account."})

        try:
            # Sign up user in Cognito
            cognito_user = self.aws_cognito_service.sign_up_user(user)
            logging.info(f"Creating new Cognito User {user.email}.")

            # Assign them to a group
            self.aws_cognito_service.add_user_to_group(user.email, DEFAULT_USER_GROUP)
            logging.info(f"Assigning new User to Group {DEFAULT_USER_GROUP}.")

            # Confirm user
            self.aws_cognito_service.confirm_user(user.email)

            # Create the user locally
            self.user_service.create_user(
                cognito_id=cognito_user["UserSub"],
                email=user.email,
                username=user.username
            )
            logging.info(f"Creating new User locally {user.email}.")
        except ClientError as e:
            self.aws_cognito_service.delete_user(user.email)
            logging.error(f"Failed to create Cognito User {user.email}: {e}")
            raise ValidationError({"error": "Failed to create a new user."})

    def sign_in_user(self, user):
        return self.aws_cognito_service.sign_in_user(user)

    def sign_out_user(self, access_token: str):
        return self.aws_cognito_service.sign_out_user(access_token=access_token)
