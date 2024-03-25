from nexong.models import PunctualDonation
from rest_framework.serializers import ModelSerializer


class PunctualDonationSerializer(ModelSerializer):
    class Meta:
        model = PunctualDonation
        fields = ["id", "name", "surname", "email", "proof_of_payment_document", "date"]
