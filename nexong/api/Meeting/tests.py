from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token


class AdminMeetingApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username="testuser", email="example1@gmail.com", role=ADMIN
        )
        self.token = Token.objects.create(user=self.user)
        self.partner1 = Partner.objects.create(
            description="testdeprueba8", address="333 Elm St", birthdate="1996-05-05"
        )
        self.partner2 = Partner.objects.create(
            description="testdeprueba10",
            address="333 Elmlos St",
            birthdate="1997-05-05",
        )
        self.meeting = Meeting.objects.create(
            name="hola", description="todo ok", date="2025-01-22", time="17:50-00:00"
        )
        self.meeting.attendees.add(self.partner1, self.partner2)

    def test_create_meeting_by_admin(self):
        attendees_ids = [self.partner1.id, self.partner2.id]
        response = self.client.post(
            f"/api/meeting/",
            data={
                "name": "Prueba2",
                "description": "Prueba meeting2",
                "date": "2025-01-22",
                "time": "17:50-00:00",
                "attendees": attendees_ids,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_meeting_error_date_by_admin(self):
        attendees_ids = [self.partner1.id, self.partner2.id]
        response = self.client.post(
            f"/api/meeting/",
            data={
                "name": "Prueba",
                "description": "Prueba meeting",
                "date": "2022-01-22",
                "time": "17:50-00:00",
                "attendees": attendees_ids,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_donations_by_admin(self):
        response = self.client.delete(
            f"/api/meeting/{self.meeting.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PartnerMeetingApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.partner3 = Partner.objects.create(
            description="testdeprueba8", address="333 Elm St", birthdate="1996-05-05"
        )
        self.user2 = User.objects.create(
            username="testuser",
            email="example1@gmail.com",
            role=PARTNER,
            partner=self.partner3,
        )
        self.token = Token.objects.create(user=self.user2)

        self.partner4 = Partner.objects.create(
            description="testdeprueba10",
            address="333 Elmlos St",
            birthdate="1997-05-05",
        )
        self.meeting2 = Meeting.objects.create(
            name="Papi", description="Chulo", date="2025-01-22", time="17:50-00:00"
        )
        self.meeting2.attendees.add(self.partner3, self.partner4)

    def test_obtain_meeting_by_partner(self):
        response = self.client.get(
            f"/api/meeting/{self.meeting2.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_meeting_by_partner(self):
        attendees_ids = [self.partner3.id, self.partner4.id]
        response = self.client.put(
            f"/api/meeting/{self.meeting2.id}/",
            data={
                "name": "Prueba Update meeting",
                "description": "Prueba Update meeting",
                "date": "2025-01-22",
                "time": "17:50-00:00",
                "attendees": attendees_ids,
                "url": f"http://localhost:8000/api/meeting/{self.meeting2.id}/",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_meeting_by_partner(self):
        attendees_ids = [self.partner3.id, self.partner4.id]
        response = self.client.post(
            f"/api/meeting/",
            data={
                "name": "Prueba3",
                "description": "Prueba meeting3",
                "date": "2025-01-22",
                "time": "17:50-00:00",
                "attendees": attendees_ids,
            },
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_meeting_by_partner(self):
        response = self.client.delete(
            f"/api/meeting/{self.meeting2.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
