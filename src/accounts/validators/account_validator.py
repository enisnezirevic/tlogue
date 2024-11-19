from accounts.models import SignUpUserModel
from accounts.validators.name_validator import NameValidator
from accounts.validators.username_validator import UsernameValidator
from utils.interfaces.validator import Validator


class AccountValidator(Validator):
    def __init__(self):
        self.first_name_validator = NameValidator(name_prefix="first_name")
        self.last_name_validator = NameValidator(name_prefix="last_name")
        self.username_validator = UsernameValidator()

    def validate(self, user: SignUpUserModel):
        self.first_name_validator.validate(user.first_name)
        self.last_name_validator.validate(user.last_name)
        self.username_validator.validate(user.username)
