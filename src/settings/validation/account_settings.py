# Default User Group
import re

DEFAULT_USER_GROUP = "Member"

# Username constraints
#     The username must:
#         - Be between 3 and 15 characters long.
#         - Start with an English letter (uppercase or lowercase).
#         - Contain only English letters, numbers, or at most one underscore.
#         - Not contain consecutive underscores.
#         - Not start or end with an underscore.
USERNAME_REGEX = re.compile(r'^[A-Za-z](?!.*__)(?!.*_$)(?!^_)[A-Za-z0-9_]{2,14}$')
