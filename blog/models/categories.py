import uuid
from django.db import models


class Category(models.Model):
    """
    this is a class to define categories for blog table
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name
