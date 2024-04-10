from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token


class AdminSuggestionApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser", email="example4@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)
        self.suggestion = Suggestion.objects.create(
            subject="Sugerencia positiva",
            description="Me gusta este sistema tan bien hecho, hablaré de esta organización a todos mis amigos.",
            date="2024-02-16",
            email="contento@gmail.com",
        )

    def test_get_suggestion_by_admin(self):
        response = self.client.get(
            f"/api/suggestion/{self.suggestion.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_suggestion_by_admin(self):
        response = self.client.delete(
            f"/api/suggestion/{self.suggestion.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
