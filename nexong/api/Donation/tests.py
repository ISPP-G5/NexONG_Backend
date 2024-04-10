from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token

class AdminDonationApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser", email="example@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)
        self.partner = Partner.objects.create(address="333 Elm St", birthdate="1996-05-05")

        self.donation = Donation.objects.create(
        iban= "ES8004875667823641839789",
        quantity= "1045.00",
        frequency= "SEMESTRAL",
        holder= "Elver Galarga",
        date= "2024-01-22",
        partner = self.partner
        )

    def test_get_donations_by_admin(self):
        response = self.client.get(
            f"/api/donation/{self.donation.id}/", HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_donations_by_admin(self):
        response = self.client.delete(
            f"/api/donation/{self.donation.id}/", HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_donations_by_admin(self):
        response = self.client.post(
            f"/api/donation/",data={
                "iban": "ES3304875667823641839789",
                "quantity": "1045.00",
                "frequency": "SEMESTRAL",
                "holder": "Elver Galarga",
                "date": "2024-01-22",
                "partner" : self.partner
                
            }, HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)