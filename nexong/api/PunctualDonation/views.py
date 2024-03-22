from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .punctualDonationSerializer import PunctualDonationSerializer
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.http import JsonResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
import json

class PunctualDonationApiViewSet(ModelViewSet):
    queryset = PunctualDonation.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = PunctualDonationSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@csrf_exempt
def process_payment(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    if request.method == 'POST':
        amount = json.loads(request.body)['amount']  # Monto en centavos
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_types=['card'],
        )
        return JsonResponse({
            'client_secret': intent.client_secret,
            'amount': amount
        })
