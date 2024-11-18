from rest_framework.exceptions import ValidationError

from accounts.services.aws_cognito_client import AwsCognitoClient
from accounts.services.aws_cognito_identity_provider import AwsCognitoIdentityProvider, SignUpUserModel
from accounts.settings.cognito_config import AwsCognitoConfig
from settings.validation.account_settings import DEFAULT_USER_GROUP


class AwsCognitoService:
    def __init__(self):
        self.client_service = AwsCognitoClient(
            aws_access_key=AwsCognitoConfig.AWS_ACCESS_KEY,
            aws_secret_access_key=AwsCognitoConfig.AWS_SECRET_ACCESS_KEY,
            region_name=AwsCognitoConfig.REGION_NAME,
            user_pool_id=AwsCognitoConfig.USER_POOL_ID
        )
        self.identity_provider = AwsCognitoIdentityProvider(
            cognito_client=self.client_service,
            client_id=AwsCognitoConfig.CLIENT_ID,
            client_secret=AwsCognitoConfig.CLIENT_SECRET
        )

    def sign_up_user(self, user: SignUpUserModel):
        """
            Create user using AWS Cognito service and assign them to default user group.

            :param user: User model containing all necessary attributes.
        """
        username_taken = self.identity_provider.is_preferred_username_taken(user.username)
        if username_taken:
            raise ValidationError({"message": "Username is already in use."})

        self.identity_provider.sign_up_user(user=user)
        self.identity_provider.add_user_to_group(email=user.email, group_name=DEFAULT_USER_GROUP)
