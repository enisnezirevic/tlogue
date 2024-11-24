from jwt import PyJWTError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.services.token_service import TokenService
from accounts.services.user_service import UserService
from followers.services.follow_service import FollowService


@api_view(["POST"])
def follow_user(request):
    user_id = request.query_params.get("user_id")
    if not user_id:
        return Response({"error": "Missing 'user_id' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # Decode token to get the current user
    try:
        token_service = TokenService()
        user_info = token_service.decode_token(access_token)
    except PyJWTError:
        return Response(
            {"error": "Invalid or expired access token."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Retrieve the follower and followed user objects
    user_service = UserService()
    follower = user_service.get_user_by_cognito_id(user_info["username"])
    if not follower:
        return Response(
            {"error": f"Authenticated user with Cognito ID {user_info['username']} not found."},
            status=status.HTTP_400_BAD_REQUEST
        )

    followed = user_service.get_user_by_cognito_id(user_id)
    if not followed:
        return Response(
            {"error": f"User with ID {user_id} not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    follow_service = FollowService()
    follow_service.follow_user(follower, followed)

    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def unfollow_user(request):
    user_id = request.query_params.get("user_id")

    if not user_id:
        return Response({"error": "Missing 'user_id' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return Response({"error": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

    # Decode token to get the current user
    try:
        token_service = TokenService()
        user_info = token_service.decode_token(access_token)
    except PyJWTError:
        return Response(
            {"error": "Invalid or expired access token."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Retrieve the follower and followed user objects
    user_service = UserService()
    follower = user_service.get_user_by_cognito_id(user_info["username"])
    if not follower:
        return Response(
            {"error": f"Authenticated user with Cognito ID {user_info['username']} not found."},
            status=status.HTTP_400_BAD_REQUEST
        )

    followed = user_service.get_user_by_cognito_id(user_id)
    if not followed:
        return Response(
            {"error": f"User with ID {user_id} not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    follow_service = FollowService()
    follow_service.unfollow_user(follower, followed)
    return Response({"message": f"Successfully unfollowed {followed.username}."}, status=status.HTTP_200_OK)


@api_view(["POST"])
def mute_user(request):
    user_id = request.query_params.get("user_id")
    if not user_id:
        return Response({"error": "Missing 'user_id' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return Response({"error": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

    # Decode token to get the current user
    try:
        token_service = TokenService()
        user_info = token_service.decode_token(access_token)
    except PyJWTError:
        return Response({"error": "Invalid or expired access token."}, status=status.HTTP_401_UNAUTHORIZED)

    user_service = UserService()
    follower = user_service.get_user_by_cognito_id(user_info["username"])
    followed = user_service.get_user_by_cognito_id(user_id)

    if not follower or not followed:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    follow_service = FollowService()
    follow_service.update_follow_properties(follower, followed, is_muted=True)

    return Response({"message": f"{followed.username} has been muted."}, status=status.HTTP_200_OK)


@api_view(["POST"])
def block_user(request):
    user_id = request.query_params.get("user_id")
    if not user_id:
        return Response({"error": "Missing 'user_id' query parameter."}, status=status.HTTP_400_BAD_REQUEST)

    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return Response({"error": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

    # Decode token to get the current user
    try:
        token_service = TokenService()
        user_info = token_service.decode_token(access_token)
    except PyJWTError:
        return Response({"error": "Invalid or expired access token."}, status=status.HTTP_401_UNAUTHORIZED)

    user_service = UserService()
    follower = user_service.get_user_by_cognito_id(user_info["username"])
    followed = user_service.get_user_by_cognito_id(user_id)

    if not follower or not followed:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    follow_service = FollowService()
    follow_service.update_follow_properties(follower, followed, is_blocked=True)

    return Response({"message": f"{followed.username} has been blocked."}, status=status.HTTP_200_OK)
