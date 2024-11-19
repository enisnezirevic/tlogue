import base64
import hashlib
import hmac

from botocore.exceptions import ClientError
from rest_framework.exceptions import ValidationError

from accounts.models import SignUpUserModel
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
        key = self.client_secret.encode()
        msg = bytes(email + self.client_id, "utf-8")
        secret_hash = base64.b64encode(
            hmac.new(key, msg, digestmod=hashlib.sha256).digest()
        ).decode()

        return secret_hash

    def sign_up_user(self, user: SignUpUserModel) -> None:
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
            self.cognito_client.get_client_instance().sign_up(**kwargs)
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidPasswordException":
                raise ValidationError({
                    "password": e.response["Error"]["Message"],
                })
            elif e.response["Error"]["Code"] == "UsernameExistsException":
                raise ValidationError({
                    "email": "This email address is associated with another account.",
                })
            else:
                raise ValidationError({
                    "message": "Sign-up failed due to unexpected error. Please try again later."
                })

    def delete_user(self, email: str) -> None:
        """
            Deletes a user from the AWS Cognito user pool.
            :param email: The email address of the user to delete.
        """
        try:
            cognito_client = self.cognito_client.get_client_instance()
            cognito_client.delete_user(UserPoolId=cognito_client.user_pool_id, Username=email)
        except ClientError as e:
            if e.response["Error"]["Code"] == "UserNotFoundException":
                raise ValidationError({"message": f"User with the username of {email} could not be found."})
            raise ValidationError({"message": f"Failed to delete the user with email {email}."})

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
        except ClientError:
            raise ValidationError({"message": "Failed to add user to group."})

    def is_preferred_username_taken(self, preferred_username: str) -> bool:
        """
        Check whether username is already in use.

        :param preferred_username: username to check.
        :return: true if existing user is using the given username, false otherwise.
        """
        try:
            response = self.cognito_client.get_client_instance().list_users(
                UserPoolId=self.cognito_client.user_pool_id,
                AttributesToGet=["preferred_username"],
                Limit=1,
                Filter=f"preferred_username = \"{preferred_username}\""
            )
            return len(response.get("Users", [])) > 0
        except ClientError:
            raise ValidationError({"message": "Failed to validate if the username is already taken."})
