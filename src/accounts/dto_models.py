from dataclasses import dataclass


@dataclass
class SignUpUserModel:
    email: str
    password: str
    username: str
    first_name: str
    last_name: str


@dataclass
class SignInUserModel:
    email: str
    password: str

@dataclass
class SignInResponse:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str
