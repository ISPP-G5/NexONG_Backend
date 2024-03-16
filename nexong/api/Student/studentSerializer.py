import datetime
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from nexong.models import Student, QuarterMarks


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

    def validate(self, data):
        if "name" in data and data["name"] == "":
            raise serializers.ValidationError("Name can't be empty")

        if "surname" in data and data["surname"] == "":
            raise serializers.ValidationError("Surname can't be empty")

        if "birthdate" in data and data["birthdate"] > datetime.date.today():
            raise serializers.ValidationError("Birthdate can't be greater than today")

        return data


class QuarterMarksSerializer(ModelSerializer):
    class Meta:
        model = QuarterMarks
        fields = "__all__"

    def validate(self, data):
        date = data["date"]
        if date > datetime.date.today():
            raise serializers.ValidationError(
                "The date in which the marks were received can't be greater than today"
            )
        return data
