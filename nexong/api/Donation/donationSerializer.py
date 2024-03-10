import re
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

    def validate(self, data):
        validation_error = {}
        iban = data["iban"]
        pattern = r"^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$"
        if not re.match(pattern, iban):
            validation_error["iban"] = "The iban does not match the expected pattern."
        if validation_error:
            raise serializers.ValidationError(validation_error)

        return data
