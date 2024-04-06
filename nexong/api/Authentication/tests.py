from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory


class FamilyApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser", email="example@gmail.com", role=ADMIN
        )
        education = EducationCenter.objects.create(name="San Francisco Solano")
        self.user1 = User.objects.create(
            username="testuser1",
            email="example1@gmail.com",
            role=EDUCATION_CENTER,
            education_center=education,
        )
        family = Family.objects.create(name="Familia López")
        self.user2 = User.objects.create(
            username="testuser2", email="example2@gmail.com", role=FAMILY, family=family
        )
        self.token = Token.objects.create(user=self.user)
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

    def test_create_family_admin(self):
        familias_creadas = Family.objects.count()
        response = self.client.post(
            "/api/family/",
            {"name": "Familia López"},
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Family.objects.count(), familias_creadas + 1)
        family = Family.objects.first()
        self.assertEqual(family.name, "Familia López")

    def test_obtain_family(self):
        family = Family.objects.create(name="Familia Lopez")
        response = self.client.get(
            f"/api/family/{family.id}/", HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Familia Lopez")

    def test_update_family(self):
        family = Family.objects.create(name="Familia López")
        response = self.client.put(
            f"/api/family/{family.id}/",
            data={"id": family.id, "name": "Familia Ruz"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token2.key}",
        )
        self.assertEqual(response.status_code, 200)
        family.refresh_from_db()
        self.assertEqual(family.name, "Familia Ruz")

    def test_delete_family(self):
        family = Family.objects.create(name="Familia Lopez")
        initial_count = Family.objects.count()
        response = self.client.delete(
            f"/api/family/{family.id}/", HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Family.objects.count(), initial_count - 1)

    def test_obtain_family_permissions_error(self):
        family = Family.objects.create(name="Familia Lopez")
        response = self.client.get(
            f"/api/family/{family.id}/", HTTP_AUTHORIZATION=f"Token {self.token1.key}"
        )
        self.assertEqual(response.status_code, 403)

    def test_update_family_permissions_error(self):
        family = Family.objects.create(name="Familia Lopez")
        response = self.client.put(
            f"/api/family/{family.id}/",
            data={"id": family.id, "name": "Familia Ruz"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token1.key}",
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_family_permissions_error(self):
        family = Family.objects.create(name="Familia Lopez")
        response = self.client.delete(
            f"/api/family/{family.id}/", HTTP_AUTHORIZATION=f"Token {self.token1.key}"
        )
        self.assertEqual(response.status_code, 403)
