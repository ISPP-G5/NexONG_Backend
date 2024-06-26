from rest_framework.exceptions import ValidationError
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from nexong.api.helpers.testsSetup import testSetupEducator
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


def add_files_to_volunteer_data(self):
    file_content = b"Test file content"  # Content of the file
    self.volunteer_data["enrollment_document"] = SimpleUploadedFile(
        "enrollment_document.pdf", file_content
    )
    self.volunteer_data["registry_sheet"] = SimpleUploadedFile(
        "registry_sheet.pdf", file_content
    )
    self.volunteer_data["sexual_offenses_document"] = SimpleUploadedFile(
        "sexual_offenses_document.pdf", file_content
    )
    self.volunteer_data["scanned_id"] = SimpleUploadedFile(
        "scanned_id.pdf", file_content
    )
    self.volunteer_data["minor_authorization"] = SimpleUploadedFile(
        "minor_authorization.pdf", file_content
    )
    self.volunteer_data["scanned_authorizer_id"] = SimpleUploadedFile(
        "scanned_authorizer_id.pdf", file_content
    )


class VolunteerApiViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.volunteer_data = {
            "academic_formation": "Test formation",
            "motivation": "Test motivation",
            "status": "ACEPTADO",
            "address": "Test address",
            "postal_code": "12345",
            "birthdate": "1956-07-05",
            "start_date": "1956-07-05",
        }
        self.volunteer3 = Volunteer.objects.create(**self.volunteer_data)
        self.user3 = User.objects.create(
            username="testuser",
            email="example@gmail.com",
            role=VOLUNTEER,
            volunteer=self.volunteer3,
        )
        self.token = Token.objects.create(user=self.user3)

    def test_create_volunteer(self):
        add_files_to_volunteer_data(self)
        response = self.client.post(
            "/api/volunteer/",
            self.volunteer_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_volunteer(self):
        response = self.client.get(
            f"/api/volunteer/{self.volunteer3.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_volunteer(self):
        add_files_to_volunteer_data(self)
        self.volunteer_data["academic_formation"] = "Updated formation"
        response = self.client.put(
            f"/api/volunteer/{self.volunteer3.id}/",
            self.volunteer_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_volunteer(self):
        response = self.client.delete(
            f"/api/volunteer/{self.volunteer3.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EducatorApiViewSetTestCase(APITestCase):
    def setUp(self):
        testSetupEducator(self)
        self.userAdmin = User.objects.create(
            username="testAdminUserForEducator",
            email="exampleAdmin@outlook.com",
            role=ADMIN,
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
        self.assertEqual(Educator.objects.count(), count + 1)
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
        self.assertEqual(Educator.objects.count(), count - 1)


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
        self.partner = Partner.objects.create(
            address="789 Oak St", birthdate="2000-10-10", description="MONDONGO"
        )
        self.user = User.objects.create(
            username="testuser",
            email="example2@gmail.com",
            role=PARTNER,
            partner=self.partner,
        )
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
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, 200)
        partner.refresh_from_db()

    def test_delete_partner(self):
        partner = Partner.objects.create(address="321 Maple St", birthdate="1970-12-12")
        initial_count = Partner.objects.count()
        response = self.client.delete(
            f"/api/partner/{partner.id}/", HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Partner.objects.count(), initial_count - 1)
