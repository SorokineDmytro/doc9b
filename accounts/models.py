from django.contrib.auth.models import AbstractUser
from django.db import models
from docs.models import UserCategory

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = ["email", "category_id"]

    category = models.ForeignKey(
        UserCategory,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="users",
    )
