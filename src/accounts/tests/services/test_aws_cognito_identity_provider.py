from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError
from rest_framework.exceptions import ValidationError

from accounts.models import SignUpUserModel
from accounts.services.aws_cognito_client import AwsCognitoClient
from accounts.services.aws_cognito_identity_provider import AwsCognitoIdentityProvider


@pytest.fixture
def aws_cognito_client():
    client = MagicMock(spec=AwsCognitoClient)
    client.get_client_instance.return_value = MagicMock()
    client.user_pool_id = "test_user_pool_id"
    return client


@pytest.fixture
def aws_identity_provider(aws_cognito_client):
    return AwsCognitoIdentityProvider(
        cognito_client=aws_cognito_client,
        client_id="test_client_id",
        client_secret="test_client_secret",
    )


@pytest.fixture
def test_user():
    return SignUpUserModel(
        email="testuser@email.com",
        password="TestPassword123!",
        username="testuser",
        first_name="TestF",
        last_name="User",
    )


def test_sign_up_user_with_valid_data_should_create_user(aws_identity_provider, aws_cognito_client, test_user):
    # Arrange
    mock_client_instance = aws_cognito_client.get_client_instance.return_value
    secret_hash_mock = "mocked_secret_hash"

    with patch.object(
        aws_identity_provider, "_AwsCognitoIdentityProvider__secret_hash", return_value=secret_hash_mock
    ):
        # Act
        aws_identity_provider.sign_up_user(test_user)

    # Assert
    mock_client_instance.sign_up.assert_called_once_with(
        ClientId="test_client_id",
        Username=test_user.email,
        Password=test_user.password,
        UserAttributes=[
            {"Name": "preferred_username", "Value": test_user.username},
            {"Name": "given_name", "Value": test_user.first_name},
            {"Name": "family_name", "Value": test_user.last_name},
        ],
        SecretHash=secret_hash_mock,
    )


def test_sign_up_user_with_invalid_data_should_raise_validation_error(aws_identity_provider, aws_cognito_client, test_user):
    # Arrange
    mock_client_instance = aws_cognito_client.get_client_instance.return_value
    mock_client_instance.sign_up.side_effect = ClientError(
        {"Error": {"Code": "SomeError", "Message": "Some error occurred"}}, "sign_up"
    )

    # Act & Assert
    with pytest.raises(ValidationError):
        aws_identity_provider.sign_up_user(test_user)


@pytest.mark.parametrize("email", ["testuser@email.com"])
def test_delete_user_with_existing_user_should_succeed(aws_identity_provider, aws_cognito_client, email):
    # Arrange
    mock_client_instance = aws_cognito_client.get_client_instance.return_value

    # Act
    aws_identity_provider.delete_user(email)

    # Assert
    mock_client_instance.admin_delete_user.assert_called_once_with(
        UserPoolId=aws_cognito_client.user_pool_id,
        Username=email,
    )


@pytest.mark.parametrize("email", ["test@email.com"])
def test_delete_user_with_nonexistent_user_should_raise_validation_error(aws_identity_provider, aws_cognito_client, email):
    # Arrange
    mock_client_instance = aws_cognito_client.get_client_instance.return_value
    mock_client_instance.admin_delete_user.side_effect = ClientError(
        {"Error": {"Code": "UserNotFoundException", "Message": "User not found"}}, "admin_delete_user"
    )

    # Act & Assert
    with pytest.raises(ValidationError):
        aws_identity_provider.delete_user(email)

    mock_client_instance.admin_delete_user.assert_called_once_with(
        UserPoolId=aws_cognito_client.user_pool_id,
        Username=email,
    )


def test_add_user_to_group_with_valid_data_should_succeed(aws_identity_provider, aws_cognito_client):
    # Arrange
    email = "user@example.com"
    group_name = "test-group"
    mock_client_instance = aws_cognito_client.get_client_instance.return_value

    # Act
    aws_identity_provider.add_user_to_group(email=email, group_name=group_name)

    # Assert
    mock_client_instance.admin_add_user_to_group.assert_called_once_with(
        UserPoolId=aws_cognito_client.user_pool_id,
        Username=email,
        GroupName=group_name,
    )


def test_add_user_to_group_with_nonexistent_user_should_raise_validation_error(aws_identity_provider, aws_cognito_client):
    # Arrange
    email = "user@example.com"
    group_name = "test-group"
    mock_client_instance = aws_cognito_client.get_client_instance.return_value
    mock_client_instance.admin_add_user_to_group.side_effect = ClientError(
        {"Error": {"Code": "UserNotFoundException", "Message": "User not found."}}, "admin_add_user_to_group"
    )

    # Act & Assert
    with pytest.raises(ValidationError):
        aws_identity_provider.add_user_to_group(email, group_name)

    mock_client_instance.admin_add_user_to_group.assert_called_once_with(
        UserPoolId=aws_cognito_client.user_pool_id,
        Username=email,
        GroupName=group_name,
    )


@pytest.mark.parametrize("username", ["testuser", "x"])
def test_is_preferred_username_taken_with_existing_username_should_return_true(aws_identity_provider, aws_cognito_client, username):
    # Arrange
    mock_client_instance = aws_cognito_client.get_client_instance.return_value
    mock_client_instance.list_users.return_value = {"Users": [{"Username": username}]}

    # Act
    result = aws_identity_provider.is_preferred_username_taken(preferred_username=username)

    # Assert
    assert result is True
    mock_client_instance.list_users.assert_called_once_with(
        UserPoolId=aws_cognito_client.user_pool_id,
        AttributesToGet=["preferred_username"],
        Limit=1,
        Filter=f'preferred_username = "{username}"',
    )


@pytest.mark.parametrize("username", ["testuser"])
def test_is_preferred_username_taken_with_nonexistent_username_should_return_false(aws_identity_provider, aws_cognito_client, username):
    # Arrange
    mock_client_instance = aws_cognito_client.get_client_instance.return_value
    mock_client_instance.list_users.return_value = {"Users": []}

    # Act
    result = aws_identity_provider.is_preferred_username_taken(preferred_username=username)

    # Assert
    assert result is False
    mock_client_instance.list_users.assert_called_once_with(
        UserPoolId=aws_cognito_client.user_pool_id,
        AttributesToGet=["preferred_username"],
        Limit=1,
        Filter=f'preferred_username = "{username}"',
    )


def test_is_preferred_username_taken_with_error_should_raise_validation_error(aws_identity_provider, aws_cognito_client):
    # Arrange
    mock_client_instance = aws_cognito_client.get_client_instance.return_value
    mock_client_instance.list_users.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "Resource not found."}}, "list_users"
    )

    # Act & Assert
    with pytest.raises(ValidationError):
        aws_identity_provider.is_preferred_username_taken("none")
