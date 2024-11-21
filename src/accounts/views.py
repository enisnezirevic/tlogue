from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.serializers import SignInUserSerializer, SignUpUserSerializer
from accounts.services.user_management_service import UserManagementService


@api_view(["POST"])
def sign_up_user(request) -> Response:
    serializer = SignUpUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_management_service = UserManagementService()
    user_management_service.create_user(serializer.create(serializer.validated_data))

    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def sign_in_user(request):
    serializer = SignInUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_management_service = UserManagementService()
    user_auth_details = user_management_service.sign_in_user(serializer.create(serializer.validated_data))

    response = Response(status=status.HTTP_200_OK)

    response.set_cookie(
        key="access_token",
        value=user_auth_details.access_token,
        httponly=True,
        max_age=user_auth_details.expires_in,
        secure=True,
        samesite="Strict",
    )

    response.set_cookie(
        key="refresh_token",
        value=user_auth_details.refresh_token,
        httponly=True,
        max_age=2592000,  # 30 Days in seconds
        secure=True,
        samesite="Strict",
    )

    return response


@api_view(["POST"])
def sign_out_user(request):
    access_token = request.COOKIES.get("access_token")

    if not access_token:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    user_management_service = UserManagementService()
    user_management_service.sign_out_user(access_token)

    response = Response(status=status.HTTP_200_OK)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return response
