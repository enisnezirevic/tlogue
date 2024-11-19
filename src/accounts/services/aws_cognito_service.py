from accounts.services.aws_cognito_client import AwsCognitoClient
from accounts.services.aws_cognito_identity_provider import AwsCognitoIdentityProvider, SignUpUserModel
from accounts.settings.cognito_config import AwsCognitoConfig
from accounts.validators.account_validator import AccountValidator
from accounts.validators.aws_cognito_validator import AwsCognitoValidator
from settings.validation.account_settings import DEFAULT_USER_GROUP
from utils.interfaces.composite_validator import CompositeValidator


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
        # Validation
        composite_validation = CompositeValidator([
            AccountValidator(),
            AwsCognitoValidator(identity_provider=self.identity_provider)
        ])
        composite_validation.validate(user)

        try:
            self.identity_provider.sign_up_user(user=user)
            self.identity_provider.add_user_to_group(email=user.email, group_name=DEFAULT_USER_GROUP)
        except Exception:
            self.identity_provider.delete_user(email=user.email)
