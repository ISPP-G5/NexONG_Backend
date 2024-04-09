import datetime
import re
from rest_framework import serializers
from nexong.models import *
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from djoser.serializers import UserCreateSerializer


class LogoutAndBlacklistSerializer(Serializer):
    refresh_token = serializers.CharField()

    class Meta:
        fields = ["refresh_token"]


class ActivateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id_number"]

    def validate_id_number(self, data):
        if not data:
            raise serializers.ValidationError("This field may not be blank.")
        pattern = r"^\d{8}[A-Z]$"
        if not re.match(pattern, data):
            raise serializers.ValidationError(
                "The id_number does not match the expected pattern."
            )
        return data


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "id_number",
            "phone",
            "password",
            "role",
            "family",
            "partner",
            "volunteer",
            "education_center",
            "educator",
            "is_agreed",
        ]

    def validate_first_name(self, data):
        if not data:
            raise serializers.ValidationError("This field may not be blank.")
        return data

    def validate_last_name(self, data):
        if not data:
            raise serializers.ValidationError("This field may not be blank.")
        return data

    def validate_id_number(self, data):
        if not data:
            raise serializers.ValidationError("This field may not be blank.")
        else:
            pattern = r"^\d{8}[A-Z]$"
            if not re.match(pattern, data):
                raise serializers.ValidationError(
                    "The id_number does not match the expected pattern."
                )
        return data

    def validate_is_agreed(self, data):
        is_agreed = data
        if is_agreed == False:
            raise serializers.ValidationError("User must accept terms and conditions.")
        return data


class UserLoginSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        fields = ["email", "password"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        validation_error = {}
        if "role" in data:
            if data["role"] == "EDUCADOR" and data["educator"] is None:
                validation_error["educator"] = (
                    'Given role "EDUCADOR", this cannot be null.'
                )
            elif data["role"] == "VOLUNTARIO" and data["volunteer"] is None:
                validation_error["volunteer"] = (
                    'Given role "VOLUNTARIO", this cannot be null.'
                )
            elif data["role"] == "FAMILIA" and data["family"] is None:
                validation_error["family"] = (
                    'Given role "FAMILIA", this cannot be null.'
                )
            elif data["role"] == "SOCIO" and data["partner"] is None:
                validation_error["partner"] = 'Given role "SOCIO", this cannot be null.'
            elif data["role"] == "VOLUNTARIO_SOCIO" and (
                data["volunteer"] is None or data["partner"] is None
            ):
                validation_error["volunteer"] = (
                    'Given role "VOLUNTARIO", this cannot be null.'
                )
                validation_error["partner"] = 'Given role "SOCIO", this cannot be null.'
        if "id_number" in data:
            id_number = data["id_number"]
            pattern = r"^\d{8}[A-Z]$"
            if not re.match(pattern, id_number):
                validation_error["id_number"] = (
                    "The id_number does not match the expected pattern."
                )
        if validation_error:
            raise serializers.ValidationError(validation_error)

        return data


class EducatorSerializer(ModelSerializer):
    class Meta:
        model = Educator
        fields = "__all__"

    def validate(self, data):
        if data["birthdate"] > datetime.date.today():
            raise serializers.ValidationError("Birthdate can't be greater than today")
        return data


class PartnerSerializer(ModelSerializer):
    class Meta:
        model = Partner
        fields = "__all__"

    def validate(self, data):
        if "birthdate" in data and data["birthdate"] > datetime.date.today():
            raise serializers.ValidationError("Birthdate can't be greater than today")
        return data


class VolunteerSerializer(ModelSerializer):
    class Meta:
        model = Volunteer
        fields = "__all__"

    def validate(self, data):
        if "birthdate" in data and data["birthdate"] > datetime.date.today():
            raise serializers.ValidationError("Birthdate can't be greater than today")

        pattern = r"^\d{5}$"
        if "postal_code" in data and not re.match(pattern, data["postal_code"]):
            raise serializers.ValidationError("Invalid postal code")
        return data


class FamilySerializer(ModelSerializer):
    class Meta:
        model = Family
        fields = "__all__"


class EducationCenterSerializer(ModelSerializer):
    class Meta:
        model = EducationCenter
        fields = "__all__"
