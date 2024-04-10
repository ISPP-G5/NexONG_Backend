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
        self.partner1 = Partner.objects.create(address="333 Elm St", birthdate="1996-05-05")
        self.partner2 = Partner.objects.create(address="333 Elmlos St", birthdate="1997-05-05")
        self.meeting = Meeting.objects.create(
            name= "hola",
            description= "todo ok",
            date= "2025-01-22",
            time = "17:50-00:00")
        self.meeting.attendees.add(self.partner1, self.partner2)
    
    def test_create_meeting_by_admin(self):
        attendees_ids = [self.partner1.id, self.partner2.id]
        response = self.client.post(
            f"/api/meeting/", data = {
                "name":"Prueba2",
                "description": "Prueba meeting2",
                "date": "2025-01-22",
                "time" : "17:50-00:00",
                "attendees": attendees_ids


            }, HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_meeting_error_date_by_admin(self):
        attendees_ids = [self.partner1.id, self.partner2.id]
        response = self.client.post(
            f"/api/meeting/", data = {
                "name":"Prueba",
                "description": "Prueba meeting",
                "date": "2022-01-22",
                "time" : "17:50-00:00",
                "attendees": attendees_ids


            }, HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_donations_by_admin(self):
        response = self.client.delete(
            f"/api/meeting/{self.meeting.id}/", HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)