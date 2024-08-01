from django_celery_beat.models import CrontabSchedule, PeriodicTask
from datetime import datetime


class Tasks:

    def crontab_schedule_delete_comments(
        self,
        name,
        minute="*",
        hour="*",
        day_of_month="*",
        month_of_year="*",
        day_of_week="*",
    ):
        crontab, created = CrontabSchedule.objects.get_or_create(
            minute=minute,  # Every minute
            hour=hour,  # Every hour
            day_of_month=day_of_month,  # Every day
            month_of_year=month_of_year,  # Every month
            day_of_week=day_of_week,  # Every day of the week
        )

        # Create the periodic task
        PeriodicTask.objects.create(
            crontab=crontab,
            name=name,
            task="comment.tasks.delete_all_comments",
            start_time=datetime.now(),  # Optional: specify when to start
        )
