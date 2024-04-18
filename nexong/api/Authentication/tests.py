from rest_framework.exceptions import ValidationError
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from nexong.api.helpers.testsSetup import testSetupEducator

class EducatorApiViewSetTestCase(APITestCase):
    def setUp(self):
        testSetupEducator(self)
        self.userAdmin = User.objects.create(
            username="testAdminUserForEducator", email="exampleAdmin@outlook.com", role=ADMIN
        )
        self.token2 = Token.objects.create(user=self.userAdmin)

    def test_create_educator(self):
        serializerE1 = EducatorSerializer(data=self.educator_error_desc)
        serializerE2 = EducatorSerializer(data=self.educator_error_date)

        response_error = self.client.post(
            "/api/educator/",
            self.educator_error_date,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token2.key}",
        )
        self.assertEqual(response_error.status_code, status.HTTP_400_BAD_REQUEST)

        with self.assertRaises(ValidationError) as context1:
            serializerE1.is_valid(raise_exception=True)
        self.assertEqual(
            context1.exception.detail["description"][0], "This field may not be blank."
        )

        with self.assertRaises(ValidationError) as context2:
            serializerE2.is_valid(raise_exception=True)
        self.assertEqual(
            context2.exception.detail["non_field_errors"][0],
            "Birthdate can't be greater than today",
        )
        
        count = Educator.objects.count()
        response = self.client.post(
            "/api/educator/",
            self.educator_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token2.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Educator.objects.count(), count+1)
        self.assertEqual(response.data["description"], "Test description")
        self.assertEqual(response.data["birthdate"], "1969-06-09")

    def test_retrieve_educator(self):
        educator = Educator.objects.create(**self.educator_data)
        response = self.client.get(
            f"/api/educator/{educator.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token2.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Test description")
        self.assertEqual(response.data["birthdate"], "1969-06-09")

    def test_update_educator(self):
        educator = Educator.objects.create(**self.educator_data)
        self.educator_data["description"] = "Updated description"
        self.educator_data["birthdate"] = "1970-07-10"
        response = self.client.put(
            f"/api/educator/{educator.id}/",
            self.educator_data,
            HTTP_AUTHORIZATION=f"Token {self.token2.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Updated description")
        self.assertEqual(response.data["birthdate"], "1970-07-10")

    def test_delete_educator(self):
        educator = Educator.objects.create(**self.educator_data)
        count = Educator.objects.count()

        response = self.client.delete(
            f"/api/educator/{educator.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token2.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Educator.objects.count(), count-1)


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
