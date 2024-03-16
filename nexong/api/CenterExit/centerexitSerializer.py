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
        lesson_event = data["lesson_event"]
        student = data["student"]
        if not lesson_event.attendees.filter(id=student.id).exists():
            raise serializers.ValidationError(
                "This student is not registered for this lesson event"
            )
        return data
