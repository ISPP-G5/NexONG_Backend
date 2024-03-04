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
