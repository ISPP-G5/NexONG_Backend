import datetime
from rest_framework import serializers
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.serializers import Serializer


class UserLoginSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        fields = ["email", "password"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


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
        if data["birthdate"] > datetime.date.today():
            raise serializers.ValidationError("Birthdate can't be greater than today")
        return data


class VolunteerSerializer(ModelSerializer):
    class Meta:
        model = Volunteer
        fields = "__all__"

    def validate(self, data):
        if data["birthdate"] > datetime.date.today():
            raise serializers.ValidationError("Birthdate can't be greater than today")
        return data


class FamilySerializer(ModelSerializer):
    class Meta:
        model = Family
        fields = "__all__"


class EducationCenterSerializer(ModelSerializer):
    class Meta:
        model = EducationCenter
        fields = "__all__"
