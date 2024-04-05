from nexong.models import Schedule
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from datetime import *
from nexong.api.helpers.serializerValidators import timezone



class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        if end_time <= start_time:
            error_message = {
                "end_time_error": ["The end time must be after start time."]
            }
            raise serializers.ValidationError(error_message)

        return attrs
