import logging

from rest_framework.exceptions import ValidationError

from accounts.services.token_service import TokenService
from accounts.services.user_management_service import UserManagementService


def token_middleware(get_response):
    def middleware(request):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        response = get_response(request)

        if access_token and refresh_token:
            try:
                token_service = TokenService()
                decoded_token = token_service.decode_token(access_token)
                expiration_timestamp = decoded_token.get("exp")

                if token_service.is_token_expired(expiration_timestamp):
                    new_token = token_service.refresh_access_token(refresh_token, decoded_token.get("username"))

                    # Update the access token
                    response.set_cookie(
                        "access_token",
                        value=new_token["AccessToken"],
                        httponly=True,
                        max_age=new_token["ExpiresIn"],
                        secure=True,
                        samesite="Strict",
                    )

                    response.delete_cookie("refresh_token")
                    logging.info("Access token refreshed, refresh token removed.")
            except Exception as e:
                user_management_service = UserManagementService()
                user_management_service.sign_out_user(access_token=access_token)
                logging.error(f"Failed to refresh access token: {e}")
                raise ValidationError(f"Failed to refresh access token: {e}")

        elif access_token:
            token_service = TokenService()
            decoded_token = token_service.decode_token(access_token)
            expiration_timestamp = decoded_token.get("exp")

            if token_service.is_token_expired(expiration_timestamp):
                user_management_service = UserManagementService()
                user_management_service.sign_out_user(access_token=access_token)
                response.delete_cookie("access_token")
                logging.info("Sign out user, token has expired.")

        return response

    return middleware
