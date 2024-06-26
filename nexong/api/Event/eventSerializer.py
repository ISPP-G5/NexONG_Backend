from rest_framework import serializers
from nexong.models import Event, LessonEvent, Student
from rest_framework.serializers import ModelSerializer
from datetime import datetime, timezone
from nexong.api.helpers.serializerValidators import date_validations


class LessonEventSerializer(ModelSerializer):
    # attendees are optional at creation
    attendees = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), many=True, required=False
    )
    url = serializers.HyperlinkedIdentityField(view_name="lessonevent-detail")

    class Meta:
        model = LessonEvent
        fields = [
            "id",
            "name",
            "description",
            "place",
            "max_volunteers",
            "start_date",
            "end_date",
            "lesson",
            "price",
            "educators",
            "attendees",
            "volunteers",
            "url",
        ]

    def validate_educators(self, value):
        if not value:
            raise serializers.ValidationError("Must provide at least 1 educator.")
        return value

    # Validations that depends on more than one parameter
    def validate(self, attrs):
        validation_error = {}

        volunteers_emails = attrs.get("volunteers")

        max_volunteers = attrs.get("max_volunteers")

        if volunteers_emails is not None:
            num_volunteers = len(volunteers_emails)
            if max_volunteers < num_volunteers:
                validation_error[
                    "max_volunteers"
                ] = "max_volunteers must be higher or equal to the number of volunteers selected."

        lesson = attrs.get("lesson")
        if lesson:
            student_lesson = lesson.students.all()
            student_lesson_ids = [student.id for student in student_lesson]
            attendees = attrs.get("attendees")
            if attendees is not None:
                for attendee in attendees:
                    if attendee.id not in student_lesson_ids:
                        validation_error[
                            "attendees"
                        ] = "The attendees must be students of the lesson selected."

        validation_error.update(date_validations(attrs))

        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        for lessonEvent in LessonEvent.objects.filter(lesson=lesson):
            if (
                (
                    start_date > lessonEvent.start_date
                    and start_date < lessonEvent.end_date
                )
                or (
                    end_date > lessonEvent.start_date
                    and end_date < lessonEvent.end_date
                )
                or (
                    start_date < lessonEvent.start_date
                    and end_date > lessonEvent.end_date
                )
            ):
                validation_error[
                    "end_date"
                ] = "Another lesson event collides with this one. Choose a different set of dates."

        if validation_error:
            raise serializers.ValidationError(validation_error)

        return attrs


class EventSerializer(ModelSerializer):
    attendees = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), many=True, required=False
    )
    url = serializers.HyperlinkedIdentityField(view_name="event-detail")

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "place",
            "max_volunteers",
            "max_attendees",
            "start_date",
            "end_date",
            "price",
            "attendees",
            "volunteers",
            "url",
        ]

    def validate(self, attrs):
        validation_error = {}

        attendees_emails = attrs.get("attendees")
        if attendees_emails is not None:
            num_attendees = len(attendees_emails)
        else:
            num_attendees = 0
        max_attendees = attrs.get("max_attendees")

        start_date = attrs.get("start_date")
        if start_date <= datetime.now(timezone.utc):
            validation_error["start_date"] = "The start date must be in the future."

        if max_attendees < num_attendees:
            validation_error[
                "max_attendees"
            ] = "max_attendees must be higher or equal to the number of attendees selected."

        volunteers = attrs.get("volunteers")
        if volunteers is not None:
            num_volunteers = len(volunteers)
        else:
            num_volunteers = 0
        max_volunteers = attrs.get("max_volunteers")

        if max_volunteers < num_volunteers:
            validation_error[
                "max_volunteers"
            ] = "max_volunteers must be higher or equal to the number of volunteers selected."

        validation_error.update(date_validations(attrs))

        if validation_error:
            raise serializers.ValidationError(validation_error)

        return attrs
