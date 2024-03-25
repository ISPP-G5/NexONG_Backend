from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ...models import *
from .punctualDonationSerializer import PunctualDonationByCardSerializer
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.http import JsonResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
import json
import requests


class PunctualDonationByCardApiViewSet(ModelViewSet):
    queryset = PunctualDonationByCard.objects.all()
    http_method_names = ["get", "post", "delete"]
    serializer_class = PunctualDonationByCardSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def process_payment(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    if request.method == "POST":
        amount = json.loads(request.body)["amount"]  # Monto en centavos
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method_types=["card"],
            payment_method="pm_card_visa",
        )
        # Confirmar la intención de pago
        try:
            intent.confirm()
        except stripe.error.CardError:
            # El pago ha fallado debido a un error en la tarjeta
            return JsonResponse(
                {
                    "error": "El pago ha fallado debido a un error en la tarjeta",
                    "status": "failed",
                }
            )
        except stripe.error.InvalidRequestError:
            # La intención de pago no es válida
            return JsonResponse(
                {"error": "La intención de pago no es válida", "status": "failed"}
            )
        except stripe.error.AuthenticationError:
            # Fallo de autenticación con Stripe
            return JsonResponse(
                {"error": "Fallo de autenticación con Stripe", "status": "failed"}
            )
        except stripe.error.APIConnectionError:
            # Error de conexión con la API de Stripe
            return JsonResponse(
                {"error": "Error de conexión con la API de Stripe", "status": "failed"}
            )
        except stripe.error.StripeError:
            # Otro tipo de error de Stripe
            return JsonResponse(
                {"error": "Error al procesar el pago con Stripe", "status": "failed"}
            )

        if intent.status == "succeeded":
            name = json.loads(request.body)["name"]
            surname = json.loads(request.body)["surname"]
            email = json.loads(request.body)["email"]
            date = json.loads(request.body)["date"]
            payload = {
                "amount": amount,
                "name": name,
                "surname": surname,
                "email": email,
                "date": date,
            }
            response = requests.post(
                "http://localhost:8000/api/punctual-donation-by-card/",
                json=payload,
                timeout=15,
            )
            if response.status_code == 200 or response.status_code == 201:
                return JsonResponse(
                    {
                        "client_secret": intent.client_secret,
                        "amount": amount,
                        "status": "succeeded",
                    }
                )
            else:
                return JsonResponse(
                    {"error": "Error al realizar la solicitud POST", "status": "failed"}
                )
        else:
            # El pago no se ha realizado correctamente
            return JsonResponse(
                {
                    "error": "El pago no se ha realizado correctamente",
                    "status": "failed",
                }
            )
