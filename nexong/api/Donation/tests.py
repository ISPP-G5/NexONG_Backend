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
            username="testuser", email="example2@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)
        self.partner = Partner.objects.create(
            description="testdeprueba2", address="333 Elm St", birthdate="1996-05-05"
        )

        self.donation = Donation.objects.create(
            iban="ES8004875667823641839789",
            quantity="1045.00",
            frequency="SEMESTRAL",
            holder="Elver Galarga",
            date="2024-01-22",
            partner=self.partner,
        )

    def test_get_donations_by_admin(self):
        response = self.client.get(
            f"/api/donation/{self.donation.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_donations_by_admin(self):
        response = self.client.delete(
            f"/api/donation/{self.donation.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_donations_by_admin(self):
        response = self.client.post(
            f"/api/donation/",
            data={
                "iban": "ES3304875667823641839789",
                "quantity": "1045.00",
                "frequency": "SEMESTRAL",
                "holder": "Elver Galarga",
                "date": "2024-01-22",
                "partner": self.partner,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PartnerDonationApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.partner2 = Partner.objects.create(
            description="testdeprueba2", address="333 Elm St", birthdate="1996-05-05"
        )
        self.user2 = User.objects.create(
            username="testuser",
            email="example2@gmail.com",
            role=PARTNER,
            partner=self.partner2,
        )
        self.token2 = Token.objects.create(user=self.user2)
        self.donation2 = Donation.objects.create(
            iban="ES8004875667823641839785",
            quantity="1054.00",
            frequency="SEMESTRAL",
            holder="Keko jones",
            date="2024-01-22",
            partner=self.partner2,
        )

    def test_get_donations_by_partner(self):
        response = self.client.get(
            f"/api/donation/{self.donation2.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token2.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_donations_by_partner(self):
        response = self.client.post(
            f"/api/donation/",
            data={
                "iban": "ES3304875667823641839785",
                "quantity": "1065",
                "frequency": "SEMESTRAL",
                "holder": "Paco Jones",
                "date": "2025-01-23",
                "partner": self.partner2.id,
            },
            HTTP_AUTHORIZATION=f"Token {self.token2.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_donations_by_partner_error(self):
        response = self.client.delete(
            f"/api/donation/{self.donation2.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token2.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
