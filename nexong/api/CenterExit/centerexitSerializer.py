import datetime
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from nexong.models import CenterExitAuthorization, LessonEvent, Student


class CenterExitSerializer(ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        many=False, required=True, queryset=Student.objects.all()
    )
    lesson_event = serializers.PrimaryKeyRelatedField(
        many=False, required=True, queryset=LessonEvent.objects.all()
    )

    class Meta:
        model = CenterExitAuthorization
        fields = "__all__"

    def validate(self, data):
        if data["date"] < datetime.date.today() or data["time"] < datetime.date.today():
            raise serializers.ValidationError("Meetings cannot be in the past")
        return data
