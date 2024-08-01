from rest_framework import serializers
from django_celery_beat.models import PeriodicTask


class CelerySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    task = serializers.CharField(max_length=500)
    start_time = serializers.CharField(max_length=500)
    total_run_count = serializers.IntegerField(read_only=True)
    date_changed = serializers.CharField(max_length=500, read_only=True)
    description = serializers.CharField(max_length=500)

    class Meta:
        model = PeriodicTask
        fields = [
            "id",
            "name",
            "task",
            "start_time",
            "total_run_count",
            "date_changed",
            "description",
        ]
