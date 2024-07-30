from celery import shared_task
from comment.models.comments import Comment


@shared_task
def delete_all_comments():
    print("task called")
    Comment.objects.all().delete()
