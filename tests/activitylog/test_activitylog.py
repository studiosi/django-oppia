# oppia/tests/tracker/test_tracker.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from oppia.models import Tracker
from tests.user_logins import *


class UploadActivityLogTest(TestCase):
    
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json',
                'default_gamification_events.json']
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('oppia_activitylog_upload')
        self.basic_activity_log = './oppia/fixtures/activity_logs/basic_activity.json'
        self.activity_log_file_path = './oppia/fixtures/activity_logs/activity_upload_test.json'
        self.wrong_activity_file = './oppia/fixtures/activity_logs/wrong_format.json'
        self.new_user_activity = './oppia/fixtures/activity_logs/new_user_activity.json'

    def test_no_file(self):
        # no file
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'activity_log_file', 'Please select an activity log file to upload')


    def test_wrong_format_file(self):
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        with open(self.wrong_activity_file, 'rb') as activity_log_file:
            response = self.client.post(self.url, { 'activity_log_file': activity_log_file })

        messages = list(response.context['messages'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertContains(response, 'wrong format')

      
    def test_correct_file(self):
        tracker_count_start = Tracker.objects.all().count()

        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        with open(self.basic_activity_log, 'rb') as activity_log_file:
            response = self.client.post(self.url, { 'activity_log_file': activity_log_file })

        self.assertRedirects(response, reverse('oppia_activitylog_upload_success'), 302,
                                 200)  # should be redirected to the update step 2 form

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)


    def test_new_user_file(self):
        tracker_count_start = Tracker.objects.all().count()
        user_count_start = User.objects.all().count()

        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        with open(self.new_user_activity, 'rb') as activity_log_file:
            response = self.client.post(self.url, { 'activity_log_file': activity_log_file })

        self.assertRedirects(response, reverse('oppia_activitylog_upload_success'), 302,
                                 200)  # should be redirected to the update step 2 form

        tracker_count_end = Tracker.objects.all().count()
        user_count_end = User.objects.all().count()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)
        self.assertEqual(user_count_start + 1, user_count_end)

