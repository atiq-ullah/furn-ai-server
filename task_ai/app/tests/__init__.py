# tests.py for your Django app

from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from unittest.mock import patch, MagicMock

# class PostPromptHandlerTests(TestCase):
#     def test_post_prompt_validation_fail(self):
#         with patch('task_ai.app.handlers.helpers.validate_request') as mock_validate:
#             mock_validate.return_value = JsonResponse({"error": "Validation failed"}, status=400)
#             response = self.client.post(reverse('post_prompt_handler'), {})
#             self.assertEqual(response.status_code, 400)

#     @patch('task_ai.app.handlers.helpers.handle_run_creation')
#     @patch('task_ai.app.handlers.periodically_check_run_status.delay')
#     def test_post_prompt_success(self, mock_check_status, mock_run_creation):
#         mock_run_creation.return_value = '12345'
#         response = self.client.post(reverse('post_prompt_handler'), {'prompt': 'test', 'p_type': 'type1'})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('run_id', response.json())

#     @patch('task_ai.app.handlers.helpers.handle_run_creation', side_effect=Exception('Test Exception'))
#     def test_post_prompt_exception(self, mock_run_creation):
#         response = self.client.post(reverse('post_prompt_handler'), {'prompt': 'test', 'p_type': 'type1'})
#         self.assertEqual(response.status_code, 500)

# class GetPromptHandlerTests(TestCase):
#     def test_get_prompt_unsupported_type(self):
#         response = self.client.get(reverse('get_prompt_handler'), {'p_type': 'unknown_type'})
#         self.assertEqual(response.status_code, 400)

#     @patch('task_ai.app.views.client.beta.threads.messages.list')
#     def test_get_prompt_success(self, mock_messages_list):
#         mock_messages_list.return_value = JsonResponse({"messages": ['Message1', 'Message2']})
#         response = self.client.get(reverse('get_prompt_handler'), {'p_type': 'type1'})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('messages', response.json())

# Add additional tests as needed

