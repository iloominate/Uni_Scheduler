from django.db import models
from django.contrib.auth.models import AbstractUser


class Permission(models.Model):
    """Table for access levels of users"""

    level = models.IntegerField()
    description = models.CharField(max_length=50)

    class Meta:
        db_table = "permission"


class User(AbstractUser):
    """Custom user for authorization app"""

    permission = models.ForeignKey(
        Permission,
        on_delete=models.PROTECT,
        related_name="user",
    )

    class Meta:
        db_table = "user"
