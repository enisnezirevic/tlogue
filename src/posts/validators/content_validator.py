from rest_framework.exceptions import ValidationError

from posts.settings.post_settings import POST_MAX_LENGTH, POST_MIN_LENGTH
from utils.interfaces.validator import Validator


class ContentValidator(Validator):
    def __init__(self):
        self.min_length = POST_MIN_LENGTH
        self.max_length = POST_MAX_LENGTH

    def validate(self, value: str):
        if len(value) < self.min_length or len(value) > self.max_length:
            raise ValidationError(f"Content must be between {self.min_length} and {self.max_length} characters long.")
