from celery import shared_task
from comment.models.comments import Comment
from datetime import datetime


@shared_task
def delete_all_comments(date_time):
    current_time = datetime.now()
    if date_time == current_time:
        Comment.objects.all().delete()
    else:
        print("task done with no action . ")
