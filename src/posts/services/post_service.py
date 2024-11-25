import logging

from rest_framework.exceptions import ValidationError

from accounts.models import User
from posts.models import Like, Post
from posts.validators.content_validator import ContentValidator


class PostService:
    def __init__(self):
        self.validator = ContentValidator()

    def create_post(self, user: User, content: str):
        """
        Creates a new post for the user with the provided content.

        :param user: The user creating the post.
        :param content: The content of the post.
        :return: True if the post was successfully created.
        """
        self.validator.validate(content)

        try:
            post = Post.objects.create(user=user, content=content)
            logging.info(f"User {user.username} created post with ID {post.id} and content: {content}")
            return True
        except Exception as e:
            logging.error(f"Error occurred while creating post. {e}")
            raise ValidationError(f"Error occurred while creating post.")

    @staticmethod
    def delete_post(user: User, post_id: int):
        """
        Deletes a post from the database.
        :param user: Creator of the post.
        :param post_id: ID of the post.
        :return: True if the post was successfully deleted.
        """
        post = Post.objects.get(id=post_id)
        if post.user.id != user.id:
            raise ValidationError(f"User {user.username} does not hold the ownership of the post.")

        post.delete()
        logging.info(f"User {user.username} deleted post with ID {post_id}.")
        return True

    @staticmethod
    def toggle_like_post(user: User, post_id: int):
        """
        Toggles the like status of a post for the user.
        If the user already liked the post, it will unlike it.
        If the user hasn't liked the post, it will create a like relationship.

        :param user: User that liked/unliked the post.
        :param post_id: ID of the post.
        :return: None
        """
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError(f"Post with ID {post_id} does not exist.")

        # Check if the user already liked the post
        existing_like = Like.objects.filter(user=user, post=post).first()

        if existing_like:
            # If already liked, remove like (unlike)
            logging.info(f"User {user.username} unliked post {post.id}.")
            existing_like.delete()
        else:
            # If not liked yet, create a like relationship
            Like.objects.create(user=user, post=post)
            logging.info(f"User {user.username} liked post {post.id}.")
