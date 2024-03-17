import datetime
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from nexong.models import Suggestion


class SuggestionSerializer(ModelSerializer):
    class Meta:
        model = Suggestion
        fields = "__all__"

    def validate(self, data):
        subject = data["subject"]
        description = data["description"]
        if subject == "":
            raise serializers.ValidationError("Subject can't be empty")
        if description == "":
            raise serializers.ValidationError("Description can't be empty")
        return data
