from datetime import datetime, timezone

import jwt
import requests
from jwt.algorithms import RSAAlgorithm

from accounts.services.aws_cognito_client import AwsCognitoClient
from accounts.services.aws_cognito_identity_provider import AwsCognitoIdentityProvider
from accounts.settings.cognito_config import AwsCognitoConfig, JWKS_URL, JWT_ALGORITHM, JWT_ISSUER


class TokenService:

    @staticmethod
    def decode_token(token: str):
        """
        Decodes the jwt token to get the payload.
        :param token: Token to decode.
        """
        # Fetch the JWKS
        response = requests.get(JWKS_URL)
        response.raise_for_status()
        jwks = response.json()

        # Extract the key ID (kid) from the token's header
        # The "kid" in the token header helps identify which key from the JWKS should be used to verify the token.
        # This is necessary because JWKS (JSON Web Key Set) can contain multiple public keys, and we need the correct one.
        unverified_header = jwt.get_unverified_header(token)
        if not unverified_header:
            raise jwt.PyJWTError("Unable to find token header.")

        kid = unverified_header.get("kid")
        if not kid:
            raise jwt.PyJWTError("Token header missing 'kid'.")

        # Find the public key in the JWKS that matches the "kid" from the token header
        # We loop through all keys in the JWKS to locate the key with a matching "kid".
        # This ensures we're using the right key to verify the token's signature.
        rsa_key = None
        for key in jwks["keys"]:
            if key["kid"] == kid:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break

        if not rsa_key:
            raise jwt.PyJWTError("Unable to find the appropriate key for token verification.")

        # Convert the JWK (JSON Web Key) to a PEM-formatted RSA public key
        # The JWK is a compact, JSON-based representation of a public key.
        # We convert it to PEM format because the decoding library (PyJWT) requires it for token verification.
        public_key = RSAAlgorithm.from_jwk(rsa_key)

        # Decode the token using the public key in PEM format
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=[JWT_ALGORITHM],
            issuer=JWT_ISSUER
        )
        return decoded_token

    @staticmethod
    def is_token_expired(expiration_timestamp):
        """
        Checks if the token has expired.
        :param expiration_timestamp: Expiration timestamp from the token.
        :return: True if the token has expired, False otherwise.
        """
        expiration_time = datetime.fromtimestamp(expiration_timestamp, tz=timezone.utc)
        current_time = datetime.now(tz=timezone.utc)
        return expiration_time < current_time

    @staticmethod
    def refresh_access_token(refresh_token, jwt_token_username):
        """
        Refresh access and ID tokens using AWS Cognito.

        :param jwt_token_username: Value of the 'username' attribute that is found inside payload data of the jwt token.
        :param refresh_token: The user's refresh token.
        :return: New tokens.
        """
        aws_cognito_identity_provider = AwsCognitoIdentityProvider(
            cognito_client=AwsCognitoClient(),
            client_id=AwsCognitoConfig.CLIENT_ID,
            client_secret=AwsCognitoConfig.CLIENT_SECRET,
        )
        return aws_cognito_identity_provider.refresh_token(refresh_token, jwt_token_username)
