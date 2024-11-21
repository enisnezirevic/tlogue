import logging

from rest_framework.exceptions import ValidationError

from accounts.models import User
from accounts.services.token_service import TokenService
from accounts.services.user_service import UserService
from followers.models import Follow


class FollowService:
    def __init__(self):
        self.token_service = TokenService()
        self.user_service = UserService()

    @staticmethod
    def follow_user(follower: User, followed: User):
        """
        Creates a follow relationship between two users.

        :param follower: The user who is following.
        :param followed: The user being followed.
        :return: True if the follow relationship was successful, False otherwise.
        """
        # Prevent a user from following themselves
        if follower.cognito_id == followed.cognito_id:
            logging.warning(f"User {follower.username} attempted to follow themselves.")
            raise ValidationError({"error": "You cannot follow yourself."})

        # Attempt to create the follow relationship
        _, created = Follow.objects.get_or_create(follower=follower, followed=followed)

        if created:
            logging.info(f"User {follower.username} successfully followed {followed.username}.")
        else:
            logging.info(f"User {follower.username} is already following {followed.username}.")
            raise ValidationError({"error": f"User {follower.username} is already following {followed.username}."})
