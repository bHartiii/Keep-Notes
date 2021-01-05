from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User, UserProfile
from Notes.models import Notes, Labels
from ..serializers import NotesSerializer
import json
from django.views.decorators.csrf import csrf_exempt

# initialize the APIClient app
client = Client(enforce_csrf_checks=True)

class NotesAPITest(TestCase):
    """ Test module for notes APIs """

    def setUp(self):
        self.user1 = User.objects.create(email='malibharti5@gmail.com', username='bharti',password='pbkdf2_sha256$180000$vf55wIVIolGs$orroOnnkyPPnUqNgUpgYK4yI9un4fl+Oy0Ig9MUF+DI=', is_active=True, is_verified=True, )
        self.user2 = User.objects.create(email='malibharti@gmail.com', username='bharti2',password='pbkdf2_sha256$180000$vf55wIVIolGs$orroOnnkyPPnUqNgUpgYK4yI9un4fl+Oy0Ig9MUF+DI=', is_active=True, is_verified=True, )
        self.note_for_user1 = Notes.objects.create(title='note1', content='first note',owner=self.user1,isArchive=False, isDelete=False)
        self.note_for_user2 = Notes.objects.create(title='user2', content='note for user 2', owner=self.user2)

        self.valid_payload = {
            'title': 'note2',
            'content': 'second note',
            'owner': self.user1.id
        }
        self.invalid_payload = {
            'title': 'note2',
            'content': ''
        }
        self.user1_credentials = {
            'email':'malibharti5@gmail.com',
            'password':'bharti'
        }
        self.invalid_credentials = {
            'email':'malibharti11@gmail.com',
            'password':'bharti'
        }

    def test_create_notes_with_valid_payload_without_login(self):
        response = client.post(reverse('notes'),data=json.dumps(self.valid_payload) ,content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_notes_with_valid_payload_after_login(self):
        client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = client.post(reverse('notes'),data=json.dumps(self.valid_payload) ,content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_notes_after_login(self):
        client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.filter(owner=self.user1, isArchive=False, isDelete=False)
        serializer = NotesSerializer(notes, many=True)
        response = client.get(reverse('notes'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_notes_of_other_user_after_login(self):
        client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.filter(owner=self.user2, isArchive=False, isDelete=False)
        serializer = NotesSerializer(notes, many=True)
        response = client.get(reverse('notes'))
        self.assertNotEqual(response.data, serializer.data)

    def test_get_notes_by_id_with_valid_payload_with_login(self):
        client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.get(id=self.note_for_user1.id)
        serializer = NotesSerializer(notes)
        response = client.get(reverse('note',kwargs={'id': self.note_for_user1.id}))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_notes_with_valid_payload_with_login(self):
        client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = client.put(reverse('note',kwargs={'id': self.note_for_user1.id}), data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)