import boto3


class AwsCognitoClient:
    """
    Class for interacting with AWS Cognito service using boto3.
    """

    def __init__(self, aws_access_key: str, aws_secret_access_key: str, region_name: str, user_pool_id: str):
        if not all([aws_access_key, aws_secret_access_key, region_name, user_pool_id]):
            raise ValueError("AWS credentials must be provided.")
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.user_pool_id = user_pool_id
        self._client = None

    def get_client_instance(self) -> boto3.client:
        """
        Lazily initializes and returns the boto3 Cognito Identity Provider client instance.

        :returns: boto3.client: The initialized boto3 client for interacting with Cognito.

        :raises botocore.exceptions.NoCredentialsError: If AWS credentials are not found.
        :raises botocore.exceptions.PartialCredentialsError: If partial credentials are provided.
        """
        if self._client is None:
            self._client = boto3.client(
                "cognito-idp",
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
        return self._client
