from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.serializers import SignUpUserSerializer
from accounts.services.aws_cognito_service import AwsCognitoService


@api_view(["POST"])
def sign_up_user(request) -> Response:
    serializer = SignUpUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    aws_cognito_service = AwsCognitoService()
    aws_cognito_service.sign_up_user(serializer.create(serializer.validated_data))

    return Response(status=status.HTTP_201_CREATED)
