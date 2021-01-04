from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, UserProfile
from ..serializers import RegisterSerializer
import json
from django.views.decorators.csrf import csrf_exempt

# initialize the APIClient app
client = Client(enforce_csrf_checks=True)

class AuthenticationAPITest(TestCase):
    """ Test module for authentication APIs """

    def setUp(self):
        user = User.objects.create(email='malibharti@gmail.com', username='bharti',password='pbkdf2_sha256$180000$vf55wIVIolGs$orroOnnkyPPnUqNgUpgYK4yI9un4fl+Oy0Ig9MUF+DI=', is_active=True, is_verified=True)
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
        self.login = {
            'email':'malibharti@gmail.com',
            'password':'bharti'
        }
        

    def test_register_user_with_valid_payload(self):
        response = client.post(reverse('register'),data=json.dumps(self.valid_payload) ,content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_register_user_with_invalid_payload(self):
        response = client.post(reverse('register'),data=json.dumps(self.invalid_payload) ,content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        response = client.post(reverse('login'), data=json.dumps(self.login), content_type='application/json',secure=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        