from nexong.models import Terms
from rest_framework.serializers import ModelSerializer
from datetime import *


class TermsSerializer(ModelSerializer):
    class Meta:
        model = Terms
        fields = "__all__"

