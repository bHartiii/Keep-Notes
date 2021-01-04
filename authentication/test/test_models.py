from django.test import TestCase
from ..models import User, UserProfile


class UserTest(TestCase):
    """ Test module for User and UserProfile models """

    def setUp(self):
        user=User.objects.create(email='bhartimali@gmail.com',username='bharti',password='bharti123')
        UserProfile.objects.create(user=user,first_name='Bharti',last_name='Mali')

    def test_create_user(self):
        user_bharti = User.objects.get(username='bharti')
        self.assertEqual(user_bharti.get_email(), "bhartimali@gmail.com")

    def test_create_user_profile(self):
        user_profile_bharti = UserProfile.objects.get(first_name='Bharti')
        self.assertEqual(user_profile_bharti.get_last_name(), "Mali")

    

       