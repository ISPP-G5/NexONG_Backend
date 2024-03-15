from rest_framework import serializers
from nexong.models import Partner
from rest_framework.serializers import ModelSerializer
from nexong.models import Meeting


class MeetingSerializer(ModelSerializer):
    attendees = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=Partner.objects.all()
    )
    url = serializers.HyperlinkedIdentityField(view_name="meeting-detail")

    class Meta:
        model = Meeting
        fields = ["id", "name", "description", "date", "time", "attendees", "url"]

    def validate(self, data):
        student = data["student"]
        lesson_event = data["lesson_event"]
        if CenterExitAuthorization.objects.filter(
            student=student, lesson_event=lesson_event
        ).exists():
            raise serializers.ValidationError(
                "An authorization for this student and lesson event already exists."
            )
        if not LessonEvent.objects.get(lesson_event).students.contains(student):
            raise serializers.ValidationError(
                "This student is not enrolled in this lesson, therefore cannot assist to this lesson event."
            )
        return data
