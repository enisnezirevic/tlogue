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

    @staticmethod
    def unfollow_user(follower: User, followed: User):
        """
        Deletes a follow relationship between two users.

        :param follower: The user who is unfollowing.
        :param followed: The user being unfollowed.
        :return: True if the unfollow relationship was successful, False otherwise.
        """
        # Ensure a valid follower and followed are provided
        if follower.cognito_id == followed.cognito_id:
            logging.warning(f"User {follower.username} attempted to unfollow themselves.")
            raise ValidationError({"error": "You cannot unfollow yourself."})

        # Attempt to delete the follow relationship
        deleted_count, _ = Follow.objects.filter(follower=follower, followed=followed).delete()

        if deleted_count > 0:
            logging.info(f"User {follower.username} successfully unfollowed {followed.username}.")
            return True
        else:
            logging.warning(
                f"User {follower.username} attempted to unfollow {followed.username}, but no follow relationship existed.")
            raise ValidationError({"error": f"You are not following {followed.username}."})

    @staticmethod
    def update_follow_properties(follower: User, followed: User, is_muted=None, is_blocked=None):
        """
        Updates the properties of a follow relationship.

        :param follower: The user performing the action.
        :param followed: The user being acted upon.
        :param is_muted: Boolean to update the is_muted property (optional).
        :param is_blocked: Boolean to update the is_blocked property (optional).
        :return: True if the update was successful.
        """
        try:
            follow = Follow.objects.get(follower=follower, followed=followed)
        except Follow.DoesNotExist:
            raise ValidationError({"error": "Follow relationship does not exist."})

        updated = False
        if is_muted is not None and follow.is_muted != is_muted:
            follow.is_muted = is_muted
            updated = True
        if is_blocked is not None and follow.is_blocked != is_blocked:
            follow.is_blocked = is_blocked
            updated = True

        if updated:
            follow.save()
            logging.info(
                f"Updated follow relationship: follower={follower.username}, followed={followed.username}, "
                f"is_muted={follow.is_muted}, is_blocked={follow.is_blocked}."
            )
        return updated
