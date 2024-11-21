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
