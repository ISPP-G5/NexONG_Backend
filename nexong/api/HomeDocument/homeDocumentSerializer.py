import re
from rest_framework import serializers
from nexong.models import HomeDocument
from rest_framework.serializers import ModelSerializer


class HomeDocumentSerializer(ModelSerializer):

    class Meta:
        model = HomeDocument
        fields = "__all__"
