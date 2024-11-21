import boto3

from accounts.settings.cognito_config import AwsCognitoConfig


class AwsCognitoClient:
    """
    Class for interacting with AWS Cognito service using boto3.
    """

    def __init__(self):
        self.aws_access_key = AwsCognitoConfig.AWS_ACCESS_KEY
        self.aws_secret_access_key = AwsCognitoConfig.AWS_SECRET_ACCESS_KEY
        self.region_name = AwsCognitoConfig.REGION_NAME
        self.user_pool_id = AwsCognitoConfig.USER_POOL_ID

    def get_client(self) -> boto3.client:
        """
        :returns: boto3.client: The initialized boto3 client for interacting with Cognito.

        :raises botocore.exceptions.NoCredentialsError: If AWS credentials are not found.
        :raises botocore.exceptions.PartialCredentialsError: If partial credentials are provided.
        """
        return boto3.client(
            "cognito-idp",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )
