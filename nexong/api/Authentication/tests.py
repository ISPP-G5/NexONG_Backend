from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token

class EducationCenterApiViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_education_center(self):
        # Obtener o crear un superusuario
        superuser, created = User.objects.get_or_create(username='admin', email='admin@example.com')
        if created:
            superuser.set_password('adminpassword')
            superuser.is_staff = True
            superuser.is_superuser = True
            superuser.save()

        # Obtener o crear el token de autenticación del superusuario
        token, created = Token.objects.get_or_create(user=superuser)
        data = {
            'name': 'Escuela Ejemplo',
        }
        url = '/api/education-center/'
        auth_header = f'Token {token.key}'
        headers = {'HTTP_AUTHORIZATION': auth_header}
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EducationCenter.objects.count(), 1)
        education_center = EducationCenter.objects.first()
        self.assertEqual(education_center.name, data['name'])
        self.assertIsInstance(EducationCenterApiViewSet.serializer_class(), EducationCenterSerializer)