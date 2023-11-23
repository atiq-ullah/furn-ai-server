import json
from unittest.mock import patch
from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from task_ai.app.handlers import post_prompt_handler, get_prompt_handler


class HandlersTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.prompt_data = {"prompt": "test prompt", "p_type": "parse"}
        self.run_id = "test_run_id"

    @patch("task_ai.app.handlers.validate_request")
    @patch("task_ai.app.handlers.handle_run_creation")
    @patch("task_ai.app.handlers.periodically_check_run_status.delay")
    def test_post_prompt_handler_success(
        self, mock_celery_delay, mock_handle_run_creation, mock_validate_request
    ):
        mock_validate_request.return_value = None
        mock_handle_run_creation.return_value = self.run_id
        mock_celery_delay.return_value = None

        request = self.factory.post("/post_prompt", self.prompt_data)
        response = post_prompt_handler(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.run_id, str(response.content))

        mock_validate_request.assert_called_once()
        mock_handle_run_creation.assert_called_once_with("parse", "test prompt")
        mock_celery_delay.assert_called_once_with("parse", self.run_id)

    @patch("task_ai.app.handlers.validate_request")
    def test_post_prompt_handler_validation_failure(self, mock_validate_request):
        mock_validate_request.return_value = JsonResponse(
            {"error": "invalid form"}, status=400
        )

        request = self.factory.post("/post_prompt", {})
        response = post_prompt_handler(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)

    @patch("task_ai.app.handlers.validate_request")
    @patch("task_ai.app.handlers.handle_run_creation")
    @patch("task_ai.app.handlers.periodically_check_run_status.delay")
    def test_post_prompt_handler_exception(
        self, mock_celery_delay, mock_handle_run_creation, mock_validate_request
    ):
        mock_celery_delay.return_value = None
        mock_validate_request.return_value = None
        mock_handle_run_creation.side_effect = ValueError("Test Exception")

        request = self.factory.post("/post_prompt", self.prompt_data)
        response = post_prompt_handler(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Test Exception", str(response.content))

    @patch("task_ai.app.handlers.client.beta.threads.messages.list")
    @patch("task_ai.app.handlers.validate_request")
    def test_get_prompt_handler_success(
        self, mock_validate_request, mock_messages_list
    ):
        mock_validate_request.return_value = None
        mock_response_data = {"messages": ["message1", "message2"]}
        mock_messages_list.return_value.json.return_value = mock_response_data

        request = self.factory.get("/get_prompt", {"p_type": "parse"})
        response = get_prompt_handler(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_data, mock_response_data)

    @patch("task_ai.app.handlers.validate_request")
    def test_get_prompt_handler_validation_failure(self, mock_validate_request):
        mock_validate_request.return_value = JsonResponse(
            {"error": "invalid form"}, status=400
        )

        request = self.factory.get("/get_prompt", {})
        response = get_prompt_handler(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)

    def test_get_prompt_handler_unsupported_type(self):
        request = self.factory.get("/get_prompt", {"p_type": "unsupported"})
        response = get_prompt_handler(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Select a valid choice. unsupported is not one of the available choices.",
            str(response.content),
        )

    # Additional test cases can be added here.
