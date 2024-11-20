import base64
import hashlib
import hmac
import logging

from botocore.exceptions import ClientError
from rest_framework.exceptions import ValidationError

from accounts.dto_models import SignUpUserModel
from accounts.services.aws_cognito_client import AwsCognitoClient


class AwsCognitoIdentityProvider:
    """
    Provides methods for user management with AWS Cognito.
    """

    def __init__(self, cognito_client: AwsCognitoClient, client_id: str, client_secret: str):
        self.cognito_client = cognito_client
        self.client_id = client_id
        self.client_secret = client_secret

    def __secret_hash(self, email: str) -> str:
        """
        Generates a secret hash for AWS Cognito authentication.

        :param email: The email address of the user.
        :return: The computed secret hash.
        """
        key = self.client_secret.encode()
        msg = bytes(email + self.client_id, "utf-8")
        secret_hash = base64.b64encode(
            hmac.new(key, msg, digestmod=hashlib.sha256).digest()
        ).decode()

        return secret_hash

    def sign_up_user(self, user: SignUpUserModel):
        """
        Signs up a user to the AWS Cognito user pool.

        :param user: The user model containing the user's sign-up details.
        :raises ValidationError: If the sign-up request fails due to invalid password or any other issue.
        """
        try:
            kwargs = {
                "ClientId": self.client_id,
                "Username": user.email,
                "Password": user.password,
                "UserAttributes": [
                    {"Name": "preferred_username", "Value": user.username},
                    {"Name": "given_name", "Value": user.first_name},
                    {"Name": "family_name", "Value": user.last_name},
                ], "SecretHash": self.__secret_hash(user.email)}
            response = self.cognito_client.get_client_instance().sign_up(**kwargs)
            logging.info(f"User {user.email} signed up successfully.")

            return response
        except ClientError as e:
            logging.error(f"Failed to sign up user {user.email}: {e.response['Error']['Message']}")
            self.__handle_client_error(error=e)

    def delete_user(self, email: str) -> None:
        """
        Deletes a user from the AWS Cognito user pool.
        :param email: The email address of the user to delete.
        """
        try:
            self.cognito_client.get_client_instance().admin_delete_user(
                UserPoolId=self.cognito_client.user_pool_id,
                Username=email
            )
            logging.info(f"User {email} deleted successfully.")
        except ClientError as e:
            logging.error(f"Failed to delete user {email}: {e.response['Error']['Message']}")
            self.__handle_client_error(error=e, attribute_name=email)

    def add_user_to_group(self, email: str, group_name: str) -> None:
        """
        Adds a user to a specified group in the AWS Cognito user pool.

        :param email: The email address of the user to be added to the group.
        :param group_name: The name of the group to which the user should be added.
        :raises ValidationError: If adding the user to the group fails.
        """
        try:
            self.cognito_client.get_client_instance().admin_add_user_to_group(
                UserPoolId=self.cognito_client.user_pool_id,
                Username=email,
                GroupName=group_name,
            )
            logging.info(f"User {email} added to group {group_name} successfully.")
        except ClientError as e:
            logging.error(f"Failed to add user {email} to group {group_name}: {e.response['Error']['Message']}")
            self.__handle_client_error(error=e)

    @staticmethod
    def __handle_client_error(error: ClientError, attribute_name: str = None) -> None:
        """
        Handles AWS Cognito ClientError exceptions by mapping error codes to ValidationError messages.

        :param error: The ClientError exception raised by AWS Cognito.
        :raises ValidationError: Custom error mapped from AWS Cognito's response.
        """
        error_code = error.response["Error"]["Code"]
        error_message = error.response["Error"]["Message"]

        error_mapping = {
            "InvalidPasswordException": error_message,
            "UserLambdaValidationException": "We could not process your registration. Please try again.",
            "ResourceNotFoundException": "Unable to process the request at this time. Please try again later.",
            "UserNotFoundException": f"User with the username '{attribute_name}' could not be found." if attribute_name else "User not found.",
        }

        # Default error message if none is found in error_mapping
        message = error_mapping.get(error_code, "An unexpected error occurred. Please try again.")

        logging.error(f"AWS Cognito error occurred: {error_code} - {error_message}")

        raise ValidationError({"message": message})
