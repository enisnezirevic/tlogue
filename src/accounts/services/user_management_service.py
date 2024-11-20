import logging

from rest_framework.exceptions import ValidationError

from accounts.services.aws_cognito_client import AwsCognitoClient
from accounts.services.aws_cognito_identity_provider import AwsCognitoIdentityProvider
from accounts.services.user_service import UserService
from accounts.settings.cognito_config import AwsCognitoConfig
from accounts.validators.account_validator import AccountValidator
from settings.validation.account_settings import DEFAULT_USER_GROUP


class UserManagementService:
    def __init__(self):
        self.aws_cognito_client = AwsCognitoClient(
            aws_access_key=AwsCognitoConfig.AWS_ACCESS_KEY,
            aws_secret_access_key=AwsCognitoConfig.AWS_SECRET_ACCESS_KEY,
            region_name=AwsCognitoConfig.REGION_NAME,
            user_pool_id=AwsCognitoConfig.USER_POOL_ID
        )
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
            self.aws_cognito_service.add_user_to_group(user.email, DEFAULT_USER_GROUP)
            logging.info(f"Creating new Cognito User {user.email}.")

            # Create the user locally
            self.user_service.create_user(
                cognito_id=cognito_user["UserSub"],
                email=user.email,
                username=user.username
            )
            logging.info(f"Creating new User locally {user.email}.")

        except Exception as e:
            self.aws_cognito_service.delete_user(user.email)
            logging.error(f"Failed to create Cognito User {user.email}: {e}")

            raise ValidationError({"error": str(e)})
