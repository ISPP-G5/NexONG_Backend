from nexong.models import PunctualDonation
from rest_framework.serializers import ModelSerializer


class PunctualDonationSerializer(ModelSerializer):
    class Meta:
        model = PunctualDonation
        fields = "__all__"
