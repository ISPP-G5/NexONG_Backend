from nexong.models import PunctualDonationByCard
from rest_framework.serializers import ModelSerializer


class PunctualDonationByCardSerializer(ModelSerializer):
    class Meta:
        model = PunctualDonationByCard
        fields = [
            "id",
            "name",
            "email",
            "amount",
            "date",
        ]
