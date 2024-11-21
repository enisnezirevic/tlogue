from accounts.models import User


class UserService:
    """
    Service designed to interact with user accounts whose information is stored in the local database.
    """

    @staticmethod
    def create_user(cognito_id, email, username):
        """
        Creates a new user account.
        :param cognito_id: The id that is assigned to the user's cognito identity.'
        :param email: Email address of the user.
        :param username: User's username.'
        :return:
        """
        User.objects.create(
            cognito_id=cognito_id,
            email=email,
            username=username,
        )

    @staticmethod
    def is_username_available(username):
        """
        Checks whether the username is available.
        :param username: Username to check.
        :return: True if the username is available, False otherwise.
        """
        if User.objects.filter(username=username).exists():
            return False

        return True

    @staticmethod
    def is_email_available(email):
        """
        Checks whether the email is available.
        :param email: Email address to check.
        :return: True if the email is available, False otherwise.
        """
        if User.objects.filter(email=email).exists():
            return False

        return True

    @staticmethod
    def get_user_by_cognito_id(cognito_id):
        if User.objects.filter(cognito_id=cognito_id).exists():
            return User.objects.get(cognito_id=cognito_id)

        return None
