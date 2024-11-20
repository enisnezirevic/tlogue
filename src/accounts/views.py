from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.serializers import SignUpUserSerializer
from accounts.services.user_management_service import UserManagementService


@api_view(["POST"])
def sign_up_user(request) -> Response:
    serializer = SignUpUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_management_service = UserManagementService()
    user_management_service.create_user(serializer.create(serializer.validated_data))

    return Response(status=status.HTTP_201_CREATED)
