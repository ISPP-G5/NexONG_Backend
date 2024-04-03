from django.test import TestCase
from nexong.api.Authentication.views import *
from nexong.models import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

class PartnerApiViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_create_partner(self):
        initial_count = Partner.objects.count()
        response = self.client.post('/api/partner/', {'address': '123 Main St', 'birthdate': '1990-01-01'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Partner.objects.count(), initial_count + 1)

    def test_retrieve_partner(self):
        partner = Partner.objects.create(address='456 Elm St', birthdate='1995-05-05')
        response = self.client.get(f'/api/partner/{partner.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['address'], '456 Elm St')

    def test_update_partner(self):
        partner = Partner.objects.create(address='789 Oak St', birthdate='2000-10-10')
        response = self.client.put(
            f'/api/partner/{partner.id}/',
            data={"id": partner.id, 'address': '789 Oak St', 'enrollment_document': None, 'birthdate': '2000-10-10'},
           content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        partner.refresh_from_db()
        self.assertEqual(partner.address, '789 Oak St')

    def test_delete_partner(self):
        partner = Partner.objects.create(address='321 Maple St', birthdate='1970-12-12')
        initial_count = Partner.objects.count()
        response = self.client.delete(f'/api/partner/{partner.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Partner.objects.count(), initial_count - 1)