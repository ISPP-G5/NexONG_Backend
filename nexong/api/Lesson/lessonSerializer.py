from rest_framework import serializers
from nexong.models import Lesson, Student, LessonAttendance
from rest_framework.serializers import ModelSerializer
from datetime import date
from nexong.api.helpers.serializerValidators import date_validations


class LessonSerializer(ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(
        many=True, required=True, queryset=Student.objects.all()
    )
    url = serializers.HyperlinkedIdentityField(view_name="lesson-detail")

    class Meta:
        model = Lesson
        fields = [
            "id",
            "name",
            "description",
            "capacity",
            "is_morning_lesson",
            "educator",
            "students",
            "start_date",
            "end_date",
            "url",
        ]

    def validate(self, attrs):
        validation_error = {}

        max_attendees = attrs.get("capacity")
        if max_attendees < 1:
            validation_error["capacity"] = "capacity must be higher than 0."
        attendees = attrs.get("students")
        if attendees:
            num_attendees = len(attendees)
        else:
            num_attendees = 0
        if max_attendees < num_attendees:
            validation_error["capacity"] = (
                "capacity must be higher or equal to the number of attendees selected."
            )

        validation_error.update(date_validations(attrs))

        if attendees is not None:
            for student in attendees:
                if student.is_morning_student != attrs.get("is_morning_lesson"):
                    validation_error["students"] = (
                        "There is a student with incorrect schedule (is a morning student or not)."
                    )

        if validation_error:
            raise serializers.ValidationError(validation_error)

        return attrs


class LessonAttendanceSerializer(ModelSerializer):
    class Meta:
        model = LessonAttendance
        fields = [
            "id",
            "date",
            "lesson",
            "volunteer",
        ]

    def validate(self, attrs):
        validation_error = {}

        dateLesson = attrs.get("date")
        if dateLesson < date.today():
            validation_error["date"] = "The date must be now or in the future."
        if validation_error:
            raise serializers.ValidationError(validation_error)

        return attrs
