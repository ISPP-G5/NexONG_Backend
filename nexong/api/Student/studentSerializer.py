import datetime
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from nexong.models import EducationCenter, Family, Student


class StudentSerializer(ModelSerializer):
    education_center = serializers.PrimaryKeyRelatedField(
        many=False, required=False, queryset=EducationCenter.objects.all()
    )
    family = serializers.PrimaryKeyRelatedField(
        many=False, required=False, queryset=Family.objects.all()
    )

    class Meta:
        model = Student
        fields = "__all__"

    def validate(self, data):
        name = data["name"]
        surname = data["surname"]

        if name == "":
            raise serializers.ValidationError("Name can't be empty")

        if surname == "":
            raise serializers.ValidationError("Surname can't be empty")

        if data["birthdate"] > datetime.date.today():
            raise serializers.ValidationError("Birthdate can't be greater than today")
        if Student.objects.filter(name=name, surname=surname).exists():
            raise serializers.ValidationError(
                "A student with this name and surname already exists."
            )

        return data
