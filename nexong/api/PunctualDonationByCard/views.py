from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .punctualDonationSerializer import PunctualDonationByCardSerializer
from ..permissions import isAdminGet
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from django.http import JsonResponse
from datetime import datetime

checkoutSessionID = None
paymentAmount = None
paymentName = None
paymentSurname = None
paymentEmail = None
paymentDate = None


class PunctualDonationByCardApiViewSet(ModelViewSet):
    queryset = PunctualDonationByCard.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = PunctualDonationByCardSerializer
    permission_classes = [isAdminGet]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(("POST",))
def process_payment(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    if request.method == "POST":
        amount = json.loads(request.body)["amount"]
        name = json.loads(request.body)["name"]
        surname = json.loads(request.body)["surname"]
        email = json.loads(request.body)["email"]
        date = datetime.today().strftime("%Y-%m-%d")
        if amount < 1:
            return Response({"msg": "La cantidad tiene que ser superior a un euro"})
        try:
            checkoutSession = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "EUR",
                            "unit_amount": int(amount) * 100,
                            "product_data": {"name": "Donación puntual"},
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=settings.URL_BASE + "api/payment/success",
                cancel_url=settings.URL_BASE + "api/payment/cancel",
            )
            global checkoutSessionID, paymentAmount, paymentName, paymentEmail, paymentDate, paymentSurname
            checkoutSessionID = checkoutSession.id
            paymentAmount = amount
            paymentName = name
            paymentEmail = email
            paymentDate = date
            paymentSurname = surname
        except Exception as e:
            return Response(
                {"msg": "Algo ha ido mal creando la sesión de Stripe", "error": str(e)},
                status=500,
            )
        return Response({"checkout_url": checkoutSession.url}, status=200)
    return Response({"msg": "El método de solicitud debe ser POST"}, status=405)


def obtainCheckoutSession():
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    global checkoutSessionID
    # Checkout session ID
    checkout_session_id = checkoutSessionID
    # Retrieve the checkout session
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
    return checkout_session


def payment_success(request):
    try:
        donation = PunctualDonationByCard.objects.create(
            name=paymentName,
            surname=paymentSurname,
            email=paymentEmail,
            amount=paymentAmount,
            date=paymentDate,
        )
        # If the creation is successful, you can perform additional actions here
        return JsonResponse({"message": f"Donacion de {donation.amount} euros creada!"})
    except Exception as e:
        # If an exception occurs during creation, handle it here
        return JsonResponse(
            {"message": f"Algo ha fallado en la creación de la donación {str(e)}"}
        )


def payment_cancel():
    return JsonResponse({"error": "Error al realizar el pago", "status": "failed"})
