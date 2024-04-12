from rest_framework.exceptions import ValidationError
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status



class EducatorApiViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.educator_data = {
            "description": "Test description",
            "birthdate": "1969-06-09",
          
        }
        self.educator_error_desc = {
            "description": "",
            "birthdate": "1969-06-09",
        }
        self.educator_error_date = {
            "description": "Test description",
            "birthdate": "2069-06-09",
        }
        self.user = User.objects.create(
            username="testuser", email="example@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)

    def test_create_educator(self):
        serializerE1 = EducatorSerializer(data = self.educator_error_desc)
        serializerE2 = EducatorSerializer(data = self.educator_error_date)

        response_error = self.client.post(
            "/api/educator/",
            self.educator_error_date,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response_error.status_code, status.HTTP_400_BAD_REQUEST)

        with self.assertRaises(ValidationError) as context1:
            serializerE1.is_valid(raise_exception=True)
        self.assertEqual(context1.exception.detail["description"][0], "This field may not be blank.")

        with self.assertRaises(ValidationError) as context2:
            serializerE2.is_valid(raise_exception=True)
        self.assertEqual(context2.exception.detail["non_field_errors"][0], "Birthdate can't be greater than today")

        response = self.client.post(
            "/api/educator/",
            self.educator_data,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Educator.objects.count(), 1)
        self.assertEqual(Educator.objects.get().description, "Test description")
        self.assertEqual(Educator.objects.get().birthdate, datetime.date(1969, 6, 9))

    def test_retrieve_educator(self):
        educator = Educator.objects.create(**self.educator_data)
        response = self.client.get(
            f"/api/educator/{educator.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
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
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Educator.objects.get().description, "Updated description"
        )
        self.assertEqual(
            Educator.objects.get().birthdate, datetime.date(1970, 7, 10)
        )


    def test_delete_educator(self):
        educator = Educator.objects.create(**self.educator_data)
        response = self.client.delete(
            f"/api/educator/{educator.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Educator.objects.count(), 0)