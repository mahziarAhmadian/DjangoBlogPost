import uuid

from django.db import models
from django.urls import reverse
from .categories import Category


class Post(models.Model):
    """
    this is a class to define posts for blog app
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title
