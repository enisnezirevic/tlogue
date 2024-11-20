from environ import environ

DEFAULT_USER_GROUP = "Member"
DEFAULT_AUTH_FLOW = "USER_PASSWORD_AUTH"

# Read AWS Connection Keys From Environment
env = environ.Env()
env.read_env(".env")


class AwsCognitoConfig:
    AWS_ACCESS_KEY = env("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    CLIENT_ID = env("COGNITO_CLIENT_ID")
    CLIENT_SECRET = env("COGNITO_CLIENT_SECRET")
    REGION_NAME = env("COGNITO_REGION_NAME")
    USER_POOL_ID = env("COGNITO_USER_POOL_ID")


# Jwt Token Settings
JWKS_URL = f"https://cognito-idp.{AwsCognitoConfig.REGION_NAME}.amazonaws.com/{AwsCognitoConfig.USER_POOL_ID}/.well-known/jwks.json"
JWT_ALGORITHM = "RS256"
JWT_ISSUER = f"https://cognito-idp.{AwsCognitoConfig.REGION_NAME}.amazonaws.com/{AwsCognitoConfig.USER_POOL_ID}"
