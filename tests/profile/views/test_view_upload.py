
from django import forms
from django.urls import reverse
from django.test import TestCase

from django.contrib.auth.models import User

from tests.user_logins import *
from tests.defaults import *

class UserUploadActivityViewTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']

    def setUp(self):
        super(UserUploadActivityViewTest, self).setUp()
        self.template = 'profile/upload.html'
        self.url = reverse('profile_upload')
        
    def test_view_upload(self):
        
        allowed_users = [ADMIN_USER]
        disallowed_users = [STAFF_USER, TEACHER_USER, NORMAL_USER]
        
        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'], password=allowed_user['password'])
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, self.template )
            self.assertEqual(response.status_code, 200)
            
        for disallowed_user in disallowed_users:
            self.client.login(username=disallowed_user['user'], password=disallowed_user['password'])
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE )
            self.assertEqual(response.status_code, 403)
