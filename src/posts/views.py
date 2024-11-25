from jwt import PyJWTError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.services.token_service import TokenService
from accounts.services.user_service import UserService
from posts.services.post_service import PostService


@api_view(["POST"])
def create_post(request):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        token_service = TokenService()
        user_info = token_service.decode_token(access_token)
    except PyJWTError:
        return Response(
            {"error": "Invalid or expired access token."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    user_service = UserService()
    user = user_service.get_user_by_cognito_id(user_info["username"])
    if not user:
        return Response(
            {"error": f"Authenticated user with Cognito ID {user_info['username']} not found."},
            status=status.HTTP_400_BAD_REQUEST
        )

    post_service = PostService()
    post_service.create_post(user, request.data["content"])

    return Response({"message": "Post was created successfully."}, status=status.HTTP_201_CREATED)
