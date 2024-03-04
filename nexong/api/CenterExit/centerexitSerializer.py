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
        student = data["student"]
        lesson_event = data["lesson_event"]
        if CenterExitAuthorization.objects.filter(
            student=student, lesson_event=lesson_event
        ).exists():
            raise serializers.ValidationError(
                "An authorization for this student and lesson event already exists."
            )
        return data
