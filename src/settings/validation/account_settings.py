# Default User Group
import re

DEFAULT_USER_GROUP = "Member"

# Name constraints
# The name must:
#     - Contain only alphabetic characters from the Latin alphabet, including accented characters (e.g., é, ñ, ü).
#     - Optionally contain spaces, hyphens, or apostrophes between parts of the name (e.g., "O'Connor", "Marie-Claire").
NAME_REGEX = re.compile(r"^[a-zA-ZÀ-ÖØ-öø-ǿ]+([ \-']?[a-zA-ZÀ-ÖØ-öø-ǿ]+)?$")

# Username constraints
# The username must:
#    - Be between 3 and 15 characters long.
#    - Start with an English letter (uppercase or lowercase).
#    - Contain only English letters, numbers, or at most one underscore.
#    - Not contain consecutive underscores.
#    - Not start or end with an underscore.
USERNAME_REGEX = re.compile(r'^[A-Za-z](?!.*__)(?!.*_$)(?!^_)[A-Za-z0-9_]{2,14}$')
