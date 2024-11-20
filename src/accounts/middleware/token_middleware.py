import logging

from accounts.services.token_service import TokenService


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
                # TODO: Sign-out user
                logging.error(f"Failed to refresh access token: {e}")

        return response

    return middleware
