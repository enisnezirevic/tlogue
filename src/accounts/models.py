from dataclasses import dataclass


@dataclass
class SignUpUserModel:
    email: str
    password: str
    username: str
    first_name: str
    last_name: str