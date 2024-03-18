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


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["email", "first_name", "last_name", "id_number", "phone", "password"]

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
        if data["role"] == "EDUCATOR" and data["educator"] is None:
            validation_error["educator"] = 'Given role "EDUCATOR", this cannot be null.'
        elif data["role"] == "VOLUNTEER" and data["volunteer"] is None:
            validation_error[
                "volunteer"
            ] = 'Given role "VOLUNTEER", this cannot be null.'
        elif data["role"] == "FAMILY" and data["family"] is None:
            validation_error["family"] = 'Given role "FAMILY", this cannot be null.'
        elif data["role"] == "PARTNER" and data["partner"] is None:
            validation_error["partner"] = 'Given role "PARTNER", this cannot be null.'
        elif data["role"] == "VOLUNTEER_PARTNER" and (
            data["volunteer"] is None or data["partner"] is None
        ):
            validation_error[
                "volunteer"
            ] = 'Given role "VOLUNTEER", this cannot be null.'
            validation_error["partner"] = 'Given role "PARTNER", this cannot be null.'

        id_number = data["id_number"]
        pattern = r"^\d{8}[A-Z]$"
        if not re.match(pattern, id_number):
            validation_error[
                "id_number"
            ] = "The id_number does not match the expected pattern."
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
