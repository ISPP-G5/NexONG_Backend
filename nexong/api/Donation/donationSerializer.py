from rest_framework import serializers
from nexong.models import Donation
from rest_framework.serializers import ModelSerializer


class DonationSerializer(ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="donation-detail")

    class Meta:
        model = Donation
        fields = [
            "id",
            "iban",
            "quantity",
            "frequency",
            "holder",
            "quota_extension_document",
            "date",
            "partner",
            "url",
        ]
