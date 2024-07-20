from django.core.management.base import BaseCommand
import random
from datetime import datetime
from accounts.models import User


class Command(BaseCommand):
    help = "inserting user"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        User.objects.create_superuser(phone_number='09122222222', password="1234")
