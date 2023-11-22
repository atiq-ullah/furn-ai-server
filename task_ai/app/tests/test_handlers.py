import json
from unittest import mock
from unittest.mock import MagicMock
from django.test import TestCase, RequestFactory

from task_ai.app.handlers.handlers import (
    list_messages,
    send_prompt,
    get_run_status,
)


class HandlersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @mock.patch("task_ai.app.handlers.handlers.client.beta.threads.messages.list")
    def test_list_messages(self, mock_messages_list):
        mock_messages_list.return_value = MagicMock()
        mock_messages_list.return_value.json.return_value = []
        request = self.factory.get("/messages/?assistant=parse")
        response = list_messages(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), json.dumps({"message": []}))

        request = self.factory.get("/messages/?assistant=cat")
        response = list_messages(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), json.dumps({"message": []}))

    @mock.patch("task_ai.app.handlers.handlers.handle_run_creation")
    @mock.patch("task_ai.app.handlers.handlers.validate_prompt_request")
    @mock.patch("task_ai.app.handlers.handlers.extract_prompt_request_data")
    def test_send_prompt(
        self, mock_extract_data, mock_validate_request, mock_handle_run
    ):
        mock_extract_data.return_value = ("test prompt", "parse")
        mock_validate_request.return_value = None
        mock_handle_run.return_value = mock.Mock(id="run_id")

        request = self.factory.post(
            "/prompt/",
            '{"prompt": "test prompt", "p_type": "parse"}',
            content_type="application/json",
        )
        response = send_prompt(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"run_id": "run_id"})

    @mock.patch("task_ai.app.handlers.handlers.client.beta.threads.runs.retrieve")
    @mock.patch("task_ai.app.handlers.handlers.client.beta.threads.messages.list")
    def test_get_run_status(self, mock_messages_list, mock_runs_retrieve):
        mock_runs_retrieve.return_value = mock.Mock(status="completed")
        mock_messages_list.return_value = MagicMock()
        mock_messages_list.return_value.json.return_value = []

        request = self.factory.get("/run_status/run_id=run_id&type=parse")
        response = get_run_status(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), json.dumps({"messages": []}))

        request = self.factory.get("/run_status/?run_id=run_id&type=cat")
        response = get_run_status(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), json.dumps({"messages": []}))


# TODO: Write tests for more scenarios
