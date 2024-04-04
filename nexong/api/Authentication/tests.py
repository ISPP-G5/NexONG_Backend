from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


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
            "status": "PENDIENTE",
            "address": "Test address",
            "postal_code": "12345",
            "birthdate": "1956-07-05",
            "start_date": "1956-07-05",
            "end_date": "1956-07-05",
        }
        add_files_to_volunteer_data(self)
        self.user = User.objects.create(
            username="testuser", email="example@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)

    def test_create_volunteer(self):
        response = self.client.post(
            "/api/volunteer/",
            self.volunteer_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Volunteer.objects.count(), 1)
        self.assertEqual(Volunteer.objects.get().academic_formation, "Test formation")

    def test_retrieve_volunteer(self):
        volunteer = Volunteer.objects.create(**self.volunteer_data)
        response = self.client.get(
            f"/api/volunteer/{volunteer.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["academic_formation"], "Test formation")

    def test_update_volunteer(self):
        volunteer = Volunteer.objects.create(**self.volunteer_data)
        add_files_to_volunteer_data(self)
        self.volunteer_data["academic_formation"] = "Updated formation"
        response = self.client.put(
            f"/api/volunteer/{volunteer.id}/",
            self.volunteer_data,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Volunteer.objects.get().academic_formation, "Updated formation"
        )

    def test_delete_volunteer(self):
        volunteer = Volunteer.objects.create(**self.volunteer_data)
        response = self.client.delete(
            f"/api/volunteer/{volunteer.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Volunteer.objects.count(), 0)
