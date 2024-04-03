from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

class FamilyApiViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_family(self):
        familias_creadas = Family.objects.count()
        response = self.client.post('/api/family/', {'name': 'Familia Lopez'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Family.objects.count(), familias_creadas + 1)
        family = Family.objects.first()
        self.assertEqual(family.name, "Familia Lopez")

    def test_obtain_family(self):
        family = Family.objects.create(name ='Familia Lopez')
        response = self.client.get(f'/api/family/{family.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Familia Lopez')

    def test_update_family(self):
        family = Family.objects.create(name ='Familia Lopez')
        response = self.client.put(f'/api/family/{family.id}/',data={"id": family.id, 'name': 'Familia Ruz'},
           content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        family.refresh_from_db()
        self.assertEqual(family.name, 'Familia Ruz')

    def test_delete_family(self):
        family = Family.objects.create(name ='Familia Lopez')
        initial_count = Family.objects.count()
        response = self.client.delete(f'/api/family/{family.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Family.objects.count(), initial_count - 1)