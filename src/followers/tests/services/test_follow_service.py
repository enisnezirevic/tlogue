import pytest
from rest_framework.exceptions import ValidationError
from accounts.models import User
from followers.models import Follow
from followers.services import follow_service
from followers.services.follow_service import FollowService


@pytest.mark.django_db
def test_follow_user_with_valid_data_should_create_follow_relationship():
    # Assign
    follower = User.objects.create(username="follower", cognito_id="follower123")
    followed = User.objects.create(username="followed", cognito_id="followed123")

    # Act
    follow_service = FollowService()
    result = follow_service.follow_user(follower, followed)

    # Assert
    assert result is None
    assert Follow.objects.filter(follower=follower, followed=followed).exists()


@pytest.mark.django_db
def test_follow_user_already_following_should_raise_error():
    # Assign
    follower = User.objects.create(username="follower", cognito_id="follower123")
    followed = User.objects.create(username="followed", cognito_id="followed123")
    Follow.objects.create(follower=follower, followed=followed)

    # Act & Assert
    follow_service = FollowService()
    with pytest.raises(ValidationError):
        follow_service.follow_user(follower, followed)


@pytest.mark.django_db
def test_follow_user_following_self_should_raise_error():
    # Assign
    user = User.objects.create(username="self_user", cognito_id="self123")

    # Act & Assert
    follow_service = FollowService()
    with pytest.raises(ValidationError):
        follow_service.follow_user(user, user)


@pytest.mark.django_db
def test_unfollow_user_with_valid_relationship_should_delete_follow():
    # Assign
    follower = User.objects.create(username="follower", cognito_id="follower123")
    followed = User.objects.create(username="followed", cognito_id="followed123")
    Follow.objects.create(follower=follower, followed=followed)

    # Act
    follow_service = FollowService()
    result = follow_service.unfollow_user(follower, followed)

    # Assert
    assert result is True
    assert not Follow.objects.filter(follower=follower, followed=followed).exists()


@pytest.mark.django_db
def test_unfollow_user_with_no_relationship_should_raise_error():
    # Assign
    follower = User.objects.create(username="follower", cognito_id="follower123")
    followed = User.objects.create(username="followed", cognito_id="followed123")

    # Act & Assert
    follow_service = FollowService()
    with pytest.raises(ValidationError):
        follow_service.unfollow_user(follower, followed)


@pytest.mark.django_db
def test_unfollow_user_unfollowing_self_should_raise_error():
    # Assign
    user = User.objects.create(username="self_user", cognito_id="self123")

    # Act & Assert
    follow_service = FollowService()
    with pytest.raises(ValidationError):
        follow_service.unfollow_user(user, user)


@pytest.mark.django_db
def test_update_follow_properties_with_valid_changes_should_update_and_return_true():
    # Assign
    follower = User.objects.create(username="follower", cognito_id="follower123")
    followed = User.objects.create(username="followed", cognito_id="followed123")
    Follow.objects.create(follower=follower, followed=followed, is_muted=False)

    # Act
    follow_service = FollowService()
    result = follow_service.update_follow_properties(follower, followed, is_muted=True)

    # Assert
    assert result is True
    assert Follow.objects.get(follower=follower, followed=followed).is_muted is True


@pytest.mark.django_db
def test_update_follow_properties_with_no_changes_should_return_false():
    # Assign
    follower = User.objects.create(username="follower", cognito_id="follower123")
    followed = User.objects.create(username="followed", cognito_id="followed123")
    Follow.objects.create(follower=follower, followed=followed, is_muted=True)

    # Act
    follow_service = FollowService()
    result = follow_service.update_follow_properties(follower, followed, is_muted=True)

    # Assert
    assert result is False

@pytest.mark.django_db
def test_update_follow_properties_follow_relationship_does_not_exist_should_raise_error():
    # Assign
    follower = User.objects.create(username="follower", cognito_id="follower123")
    followed = User.objects.create(username="followed", cognito_id="followed123")

    follow_service = FollowService()

    # Act & Assert
    with pytest.raises(ValidationError):
        follow_service.update_follow_properties(follower, followed, is_muted=True)

