from environ import environ

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
