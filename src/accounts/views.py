from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import SignUpUserModel
from accounts.services.aws_cognito_service import AwsCognitoService


@api_view(["POST"])
def sign_up_user(request) -> Response:
    email = request.data.get("email")
    password = request.data.get("password")
    username = request.data.get("username")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    user = SignUpUserModel(
        email=email,
        password=password,
        username=username,
        first_name=first_name,
        last_name=last_name
    )

    aws_cognito_service = AwsCognitoService()
    aws_cognito_service.sign_up_user(user)

    return Response(status=status.HTTP_201_CREATED)
