from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token


class AdminPuntualDonationApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser", email="example@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)
        file_content = b"Test file content"

        self.puntualdonation = PunctualDonation.objects.create(
            name="Prueba puntual",
            surname="Prueba 2",
            email="example2@gmail.com",
            proof_of_payment_document=SimpleUploadedFile(
                "proof_of_payment_document.pdf", file_content
            ),
            date="2024-01-22",
        )

    def test_get_puntual_donations_by_admin(self):
        response = self.client.get(
            f"/api/punctual-donation/{self.puntualdonation.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_puntual_donations_by_admin(self):
        response = self.client.delete(
            f"/api/punctual-donation/{self.puntualdonation.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
