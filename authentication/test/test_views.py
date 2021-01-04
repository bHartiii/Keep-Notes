from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, UserProfile
from ..serializers import RegisterSerializer
import json


# initialize the APIClient app
client = Client(enforce_csrf_checks=True)

class RegisterUserAPITest(TestCase):
    """ Test module for Register user API """

    def setUp(self):
        self.valid_payload = {
            'email': 'malichandni5@gmail.com',
            'username': 'bharti1',
            'password': 'bharti1',
            'profile': {
                'first_name': 'bharti',
                'last_name': 'mali',
                'DOB': None,
                'image': None
            }
        }
        self.invalid_payload = {
            'email': '',
            'username': 'bharti1',
            'password': 'bharti1',
            'profile': {
                'first_name': 'bharti',
                'last_name': 'mali',
                'DOB': None,
                'image': None
            }
        }

    def test_register_user_with_valid_payload(self):
        response = client.post(reverse('register'),data=json.dumps(self.valid_payload) ,content_type='application/json', follow=True, secure=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_register_user_with_invalid_payload(self):
        response = client.post(reverse('register'),data=json.dumps(self.invalid_payload) ,content_type='application/json', follow=True, secure=False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
