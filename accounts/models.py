from django.contrib.auth.models import AbstractUser
from django.db import models
from docs.models import UserCategory

class CustomUser(AbstractUser):
    category = models.ForeignKey(
        UserCategory,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="users",
    )
