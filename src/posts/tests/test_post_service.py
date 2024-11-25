from unittest.mock import Mock

import pytest
from rest_framework.exceptions import ValidationError

from accounts.models import User
from posts.models import Like, Post
from posts.services.post_service import PostService
from posts.validators.content_validator import ContentValidator


@pytest.mark.django_db
def test_create_post_success():
    # Assign
    user = User.objects.create(username="testuser", cognito_id="user123")
    content = "This is a test post."
    mock_validator = Mock(ContentValidator)
    mock_validator.validate.return_value = None
    post_service = PostService()

    # Act
    result = post_service.create_post(user, content)

    # Assert
    assert result is True
    assert Post.objects.filter(user=user, content=content).exists()


@pytest.mark.django_db
def test_create_post_validation_error():
    # Assign
    user = User.objects.create(username="testuser", cognito_id="user123")
    invalid_content = ""
    mock_validator = Mock(ContentValidator)
    mock_validator.validate.side_effect = ValidationError()
    post_service = PostService()

    # Act & Assert
    with pytest.raises(ValidationError):
        post_service.create_post(user, invalid_content)


@pytest.mark.django_db
def test_delete_post_success():
    # Assign
    user = User.objects.create(username="user1", cognito_id="user123")
    post = Post.objects.create(user=user, content="Test post content")

    # Act
    result = PostService.delete_post(user, post.id)

    # Assert
    assert result is True
    assert not Post.objects.filter(id=post.id).exists()


@pytest.mark.django_db
def test_delete_post_user_not_owner():
    # Assign
    user1 = User.objects.create(username="user1", cognito_id="user123")
    user2 = User.objects.create(username="user2", cognito_id="user456")
    post = Post.objects.create(user=user1, content="Test post content")

    # Act & Assert
    with pytest.raises(ValidationError):
        PostService.delete_post(user2, post.id)


@pytest.mark.django_db
def test_toggle_like_post_like():
    # Assign
    user = User.objects.create(username="user1", cognito_id="user123")
    post = Post.objects.create(user=user, content="Test post content")

    # Act
    result = PostService.toggle_like_post(user, post.id)

    # Assert
    assert result is None  # No return value expected
    assert Like.objects.filter(user=user, post=post).exists()


@pytest.mark.django_db
def test_toggle_like_post_unlike():
    # Assign
    user = User.objects.create(username="user1", cognito_id="user123")
    post = Post.objects.create(user=user, content="Test post content")
    Like.objects.create(user=user, post=post)

    # Act
    result = PostService.toggle_like_post(user, post.id)

    # Assert
    assert result is None
    assert not Like.objects.filter(user=user, post=post).exists()


@pytest.mark.django_db
def test_toggle_like_post_post_not_found():
    # Assign
    user = User.objects.create(username="user1", cognito_id="user123")
    invalid_post_id = -1

    # Act & Assert
    with pytest.raises(ValidationError):
        PostService.toggle_like_post(user, invalid_post_id)


@pytest.mark.django_db
def test_toggle_like_post_already_liked():
    # Assign
    user = User.objects.create(username="user1", cognito_id="user123")
    post = Post.objects.create(user=user, content="Test post content")
    Like.objects.create(user=user, post=post)

    # Act & Assert
    result = PostService.toggle_like_post(user, post.id)
    assert result is None
    assert not Like.objects.filter(user=user, post=post).exists()
