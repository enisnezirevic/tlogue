from django.db import models


class User(models.Model):
    cognito_id = models.CharField(unique=True, max_length=255)
    email = models.EmailField()
    username = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.email
