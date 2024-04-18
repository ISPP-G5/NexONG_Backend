from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APITestCase
from rest_framework import status
from nexong.api.helpers.testsSetup import testSetupEducator


class EducatorCenterExitApiViewSetTestCase(APITestCase):
    def setUp(self):
        testSetupEducator(self)
       

    def test_create_center_exit_by_educator(self):
        response = self.client.post(
            "/api/center-exit/",
            self.center_exit,
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_obtain_center_authorization_by_educator(self):
        center_exit = CenterExitAuthorization.objects.create(**self.center_exit)
        response = self.client.get(
            f"/api/center-exit/{center_exit.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(center_exit.is_authorized, True)

    def test_update_center_authorization_by_educator(self):
        center_exit = CenterExitAuthorization.objects.create(**self.center_exit)
        self.center_exit["is_authorized"] = False
        response = self.client.put(
            f"/api/center-exit/{center_exit.id}/",
            self.center_exit,
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_center_authorization_by_educator(self):
        center_exit = CenterExitAuthorization.objects.create(**self.center_exit)
        response = self.client.delete(
            f"/api/center-exit/{center_exit.id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
