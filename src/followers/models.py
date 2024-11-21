from django.db import models

from accounts.models import User


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_muted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
