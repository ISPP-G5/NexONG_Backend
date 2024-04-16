from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token


class AdminUserApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testu", email="example10@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)

        self.family = Family.objects.create(name="Familia López")
        self.userfamily = User.objects.create(
            username="testuser2",
            email="example2@gmail.com",
            role=FAMILY,
            family=self.family,
        )
        self.education_center = EducationCenter.objects.create(
            name="San Antonio Lobato"
        )
        self.partner = Partner.objects.create(
            description="testdeprueba", address="333 ALO", birthdate="1981-06-21"
        )
        self.educator = Educator.objects.create(
            description="testdeprueba", birthdate="2000-04-21"
        )
        self.volunteer = Volunteer.objects.create(
            academic_formation="Voluntario Admin ",
            motivation="Voluntario Admin",
            status="PENDIENTE",
            address="Voluntario Admin",
            postal_code=12350,
            birthdate="1957-07-05",
            start_date="1960-07-05",
            end_date="1980-07-05",
        )

    def test_get_user_by_admin(self):
        response = self.client.get(
            f"/api/user/{self.userfamily.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_user_by_admin(self):
        response = self.client.put(
            f"/api/user/{self.userfamily.id}/",
            data={
                "first_name": "",
                "last_name": "",
                "is_staff": False,
                "is_active": True,
                "date_joined": "2024-03-20T13:06:09.673795Z",
                "username": "testuser3",
                "id_number": "85738237V",
                "phone": 638576655,
                "password": "admin",
                "email": "admin@gmail.com",
                "role": "ADMIN",
                "is_enabled": True,
                "is_agreed": False,
                "terms_version_accepted": 1.0,
                "family": self.family.id,
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.userfamily.refresh_from_db()
        self.assertEqual(self.userfamily.username, "testuser3")

    def test_delete_user_by_admin(self):
        response = self.client.delete(
            f"/api/user/{self.userfamily.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_educator_by_admin(self):
        response = self.client.get(
            f"/api/educator/{self.educator.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_get_partner_by_admin(self):
        response = self.client.get(
            f"/api/educator/{self.partner.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_get_volunteer_by_admin(self):
        response = self.client.get(
            f"/api/educator/{self.volunteer.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_get_education_center_by_admin(self):
        response = self.client.get(
            f"/api/education-center/{self.education_center.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_create_education_center_by_admin(self):
        response = self.client.post(
            f"/api/education-center/",
            data={"name": "San Carlos"},
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 201)

    def test_create_education_center_error_by_admin(self):
        response = self.client.post(
            f"/api/education-center/",
            data={"name": ""},
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_education_center_by_admin(self):
        response = self.client.put(
            f"/api/education-center/{self.education_center.id}/",
            data={"name": "San Fisichella"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_education_center_error_by_admin(self):
        response = self.client.put(
            f"/api/education-center/{self.education_center.id}/",
            data={"name": ""},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_education_center_error_by_admin(self):
        response = self.client.delete(
            f"/api/education-center/{self.education_center.id}/",
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 204)

class PartnerApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.partner = Partner.objects.create(address="789 Oak St", birthdate="2000-10-10", description="MONDONGO")
        self.user = User.objects.create(username = 'testuser', email = "example2@gmail.com", role = PARTNER, partner=self.partner)
        self.token = Token.objects.create(user=self.user)

    def test_update_partner(self):
        partner = Partner.objects.create(address="789 Oak St", birthdate="2000-10-10")
        response = self.client.put(
            f"/api/partner/{partner.id}/",
            data={
                "id": partner.id,
                "address": "789 Oak St",
                "enrollment_document": None,
                "description": "Mondongo",
                "birthdate": "2000-10-10",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, 200)
        partner.refresh_from_db()

    def test_delete_partner(self):
        partner = Partner.objects.create(address="321 Maple St", birthdate="1970-12-12")
        initial_count = Partner.objects.count()
        response = self.client.delete(f"/api/partner/{partner.id}/", HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Partner.objects.count(), initial_count - 1)
