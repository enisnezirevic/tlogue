from unittest.mock import MagicMock, patch

import pytest

from accounts.services.aws_cognito_client import AwsCognitoClient

AWS_ACCESS_KEY = "test-access-key"
AWS_SECRET_ACCESS_KEY = "test-secret-key"
REGION_NAME = "us-west-1"
USER_POOL_ID = "test-user-pool-id"


@pytest.fixture
def aws_credentials():
    return {
        "aws_access_key": AWS_ACCESS_KEY,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region_name": REGION_NAME,
        "user_pool_id": USER_POOL_ID,
    }


def test_aws_cognito_client_initialization(aws_credentials):
    client = AwsCognitoClient(**aws_credentials)
    assert client.aws_access_key == AWS_ACCESS_KEY
    assert client.aws_secret_access_key == AWS_SECRET_ACCESS_KEY
    assert client.region_name == REGION_NAME
    assert client.user_pool_id == USER_POOL_ID
    assert client._client is None  # AwsCognitoClient class uses lazy loading


def test_aws_cognito_client_missing_credentials():
    with pytest.raises(ValueError, match="AWS credentials must be provided."):
        AwsCognitoClient("", None, "", None)

@patch("boto3.client")
def test_aws_cognito_client_instance_lazy_initialization(mock_cognito_client, aws_credentials):
    mock_client_instance = MagicMock()
    mock_cognito_client.return_value = mock_client_instance

    client = AwsCognitoClient(**aws_credentials)

    cognito_client = client.get_client_instance()
    mock_cognito_client.assert_called_once_with(
        "cognito-idp",
        aws_access_key_id=aws_credentials["aws_access_key"],
        aws_secret_access_key=aws_credentials["aws_secret_access_key"],
        region_name=aws_credentials["region_name"],
    )
    assert cognito_client == mock_client_instance

    # Second call should return the same client instance without reinitializing
    cognito_client_again = client.get_client_instance()
    mock_cognito_client.assert_called_once()  # Ensure no new calls were made
    assert cognito_client_again == cognito_client
