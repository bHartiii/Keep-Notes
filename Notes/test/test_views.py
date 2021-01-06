from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import User, UserProfile
from Notes.models import Notes, Labels
from ..serializers import NotesSerializer, LabelsSerializer
import json
from django.views.decorators.csrf import csrf_exempt



class GetNotesAPITest(TestCase):
    """ Test module for notes APIs """
       
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(email='malibharti5@gmail.com', username='bharti',password='pbkdf2_sha256$180000$vf55wIVIolGs$orroOnnkyPPnUqNgUpgYK4yI9un4fl+Oy0Ig9MUF+DI=', is_active=True, is_verified=True, )
        self.user2 = User.objects.create(email='malibharti@gmail.com', username='bharti2',password='pbkdf2_sha256$180000$vf55wIVIolGs$orroOnnkyPPnUqNgUpgYK4yI9un4fl+Oy0Ig9MUF+DI=', is_active=True, is_verified=True, )
        self.note_for_user1 = Notes.objects.create(title='note1', content='first note',owner=self.user1,isArchive=False, isDelete=False)
        self.note_for_user2 = Notes.objects.create(title='user2', content='note for user 2', owner=self.user2)
        self.label_for_user1 = Labels.objects.create(name='label1', owner=self.user1)
        self.label_for_user2 = Labels.objects.create(name='label2', owner=self.user2)

        self.valid_payload = {
            'title': 'test',
            'content': 'test'
        }
        self.invalid_payload = {
            'title': 'note2',
            'content': ''
        }
        self.valid_label_payload = {
           'name': 'test label'
        }
        self.invalid_label_payload = {
            'name' : None
        }
        self.user1_credentials = {
            'email':'malibharti5@gmail.com',
            'password':'bharti'
        }
        self.invalid_credentials = {
            'email':'malibharti11@gmail.com',
            'password':'bharti'
        }

### create and listing notes test cases:

    def test_get_all_notes_without_login(self):
        notes = Notes.objects.filter(owner=self.user1, isArchive=False, isDelete=False)
        response = self.client.get(reverse('notes'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_notes_after_login_with_invalid_credentials(self):
        self.client.post(reverse('login'),data=json.dumps(self.invalid_credentials), content_type='application/json')
        response = self.client.get(reverse('notes'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_notes_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.filter(owner=self.user1, isArchive=False, isDelete=False)
        serializer = NotesSerializer(notes, many=True)
        response = self.client.get(reverse('notes'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_notes_of_other_user_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.filter(owner=self.user2, isArchive=False, isDelete=False)
        serializer = NotesSerializer(notes, many=True)
        response = self.client.get(reverse('notes'))
        self.assertNotEqual(response.data, serializer.data)

    def test_get_all_notes_of_with_IsDelete_value_true_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.filter(owner=self.user1, isArchive=False, isDelete=True)
        serializer = NotesSerializer(notes, many=True)
        response = self.client.get(reverse('notes'))
        self.assertNotEqual(response.data, serializer.data)

    def test_create_notes_with_valid_payload_without_login(self):
        response = self.client.post(reverse('notes'),data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_notes_with_valid_payload_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.post(reverse('notes'),data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_notes_with_invalid_payload_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.post(reverse('notes'),data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

### Test cases for retrieve, update and delete note by id: 

    def test_get_notes_by_id_without_login(self):
        response = self.client.get(reverse('note',kwargs={'id': self.note_for_user1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_notes_by_id_after_login_with_invalid_credentials(self):
        self.client.post(reverse('login'),data=json.dumps(self.invalid_credentials), content_type='application/json')
        response = self.client.get(reverse('note',kwargs={'id': self.note_for_user1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_notes_by_id_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        notes = Notes.objects.get(id=self.note_for_user1.id)
        serializer = NotesSerializer(notes)
        response = self.client.get(reverse('note',kwargs={'id': self.note_for_user1.id}))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_notes_by_id_of_other_user_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.get(reverse('note',kwargs={'id': self.note_for_user2.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_notes_with_valid_payload_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.put(reverse('note',kwargs={'id':self.note_for_user1.id}), data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_notes_with_invalid_payload_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.put(reverse('note',kwargs={'id':self.note_for_user1.id}), data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_note_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.delete(reverse('note',kwargs={'id':self.note_for_user1.id}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_note_of_other_user_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.delete(reverse('note',kwargs={'id':self.label_for_user2.id}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note_without_login(self):
        response = self.client.delete(reverse('note',kwargs={'id':self.note_for_user1.id}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

### test cases for create and list label: 

    def test_get_all_labels_after_login_with_invalid_credentials(self):
        self.client.post(reverse('login'),data=json.dumps(self.invalid_credentials), content_type='application/json')
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_labels_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        labels = Labels.objects.filter(owner=self.user1)
        serializer = LabelsSerializer(labels, many=True)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_labels_without_login(self):
        labels = Labels.objects.filter(owner=self.user1)
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_labels_of_other_user_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        labels = Labels.objects.filter(owner=self.user2)
        serializer = LabelsSerializer(labels, many=True)
        response = self.client.get(reverse('labels'))
        self.assertNotEqual(response.data, serializer.data)

### Test cases for retrieve, update and delete label by id:

    def test_get_labels_by_id_without_login(self):
        response = self.client.get(reverse('label',kwargs={'id': self.label_for_user1.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_labels_by_id_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        labels = Labels.objects.get(id=self.label_for_user1.id)
        serializer = LabelsSerializer(labels)
        response = self.client.get(reverse('label',kwargs={'id': self.label_for_user1.id}))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_label_without_login(self):
        response = self.client.post(reverse('labels'),data=json.dumps(self.valid_label_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_labels_with_valid_payload_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.post(reverse('labels'),data=json.dumps(self.valid_label_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_label_with_valid_payload_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.put(reverse('label',kwargs={'id':self.label_for_user1.id}), data=json.dumps(self.valid_label_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_label_with_invalid_payload_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.put(reverse('label',kwargs={'id':self.label_for_user1.id}), data=json.dumps(self.invalid_label_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_label_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.delete(reverse('label',kwargs={'id':self.label_for_user1.id}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_label_of_other_user_after_login(self):
        self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
        response = self.client.delete(reverse('label',kwargs={'id':self.label_for_user2.id}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note_without_login(self):
        response = self.client.delete(reverse('label',kwargs={'id':self.label_for_user1.id}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)