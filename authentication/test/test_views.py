from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, UserProfile
from ..serializers import RegisterSerializer
import json
from django.views.decorators.csrf import csrf_exempt



class AuthenticationAPITest(TestCase):
    """ Test module for authentication APIs """

    def setUp(self):
        # initialize the APIClient app
        self.client = Client()
        user = User.objects.create(email='malichandni5@gmail.com', username='bharti',password='pbkdf2_sha256$180000$vf55wIVIolGs$orroOnnkyPPnUqNgUpgYK4yI9un4fl+Oy0Ig9MUF+DI=', is_active=True, is_verified=True)
        UserProfile.objects.update(user=user, first_name="bharti")
        self.valid_profile_payload = {
            'first_name': 'bharti',
            'last_name': 'mali',
            'DOB': None,
            'image': None
        }
        self.invalid_profile_payload = {
            'first_name': None,
            'last_name': 'mali',
            'DOB': None,
            'image': None
        }

        self.valid_payload = {
            'email': 'malibharti5@gmail.com',
            'username': 'bharti',
            'password': 'bharti',
        }
        self.invalid_payload = {
            'email': '',
            'username': 'bharti1',
            'password': 'bharti1',
        }
        self.valid_credentials = {
            'email':'malichandni5@gmail.com',
            'password':'bharti'
        }
        self.invalid_credentials = {
            'email':'malibharti11@gmail.com',
            'password':'bharti'
        }

    def test_register_user_with_valid_payload(self):
        response = self.client.post(reverse('register'),data=json.dumps(self.valid_payload) ,content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_register_user_with_invalid_payload(self):
        response = self.client.post(reverse('register'),data=json.dumps(self.invalid_payload) ,content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_verify_email_with_valid_token(self):
        response = self.client.post(reverse('register'),data=json.dumps(self.valid_payload) ,content_type='application/json')
        token = response.data['token']
        res = self.client.get('http://localhost:8000/auth/verify-email/?token='+token, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_verify_email_with_invalid_token(self):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo3LCJ1c2VybmFtZSI6Im1hbGljaGFuZG5pNUBnbWFpbC5jb20iLCJleHAiOjE2MDk4Njc5NDIsImVtYWlsIjoibWFsaWNoYW5kbmk1QGdtYWlsLmNvbSJ9.anw9BbFTJSjVa4j9Jur8YLQM-CNSVW2O4Zwm7xnBO"
        res = self.client.get('http://localhost:8000/auth/verify-email/?token='+token, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('login'), data=json.dumps(self.valid_credentials), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), data=json.dumps(self.invalid_credentials), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_logout(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_credentials), content_type='application/json')
        response = self.client.get(reverse('logout'),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_with_invalid_credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.invalid_credentials), content_type='application/json')
        response = self.client.get(reverse('logout'),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_without_login(self):
        response = self.client.get(reverse('logout'),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_profile_retrieve(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_credentials), content_type='application/json')
        response = self.client.get(reverse('user-profile'), content_type='application/json')
        self.assertEqual(response.data['first_name'], "bharti")
        self.assertEqual(response.data['last_name'], "")
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_user_profile_retrieve_without_login(self):
        response = self.client.get(reverse('user-profile'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_user_update_its_user_profile_valid_payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_credentials), content_type='application/json')
        response = self.client.put(reverse('user-profile'), data=json.dumps(self.valid_profile_payload) ,content_type='application/json', secure=False, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    

    def test_user_update_its_user_profile_with_invalid_payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.valid_credentials), content_type='application/json')
        response = self.client.put(reverse('user-profile'), data=json.dumps(self.invalid_profile_payload) ,content_type='application/json',  secure=False, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 