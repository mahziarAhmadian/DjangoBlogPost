import uuid
from django.db import models
from blog.models.posts import Post
from accounts.models.profile import Profile
from datetime import datetime


class Comment(models.Model):
    """
    this is a class to define categories for blog table
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content = models.TextField()
    comment_level = models.IntegerField(null=True)
    create_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.id)

    def get_level(self):
        level = 0
        project = self
        while project.parent:
            project = project.parent
            level += 1
        return level

    def get_descendants(self):
        descendants = []
        children = self.children.all()
        for child in children:
            descendants.append(child)
        return descendants

    def save(self, *args, **kwargs):
        # Calculate the comment level before saving
        self.comment_level = self.get_level()
        super().save(*args, **kwargs)
