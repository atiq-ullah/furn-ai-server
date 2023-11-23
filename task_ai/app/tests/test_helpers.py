from django import forms
from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from unittest import mock


from task_ai.app.handlers.helpers import (
    handle_run_creation,
    validate_request,
    PromptForm,
)


class InputForm(forms.Form):
    prompt = forms.CharField(required=False)
    p_type = forms.CharField(required=False)


class MockRun:
    def __init__(self, id):
        self.id = id
        self.status = "completed"


class HelpersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_validate_request_valid(self):
        encoded_data = PromptForm(
            {
                "p_type": "parse",
                "prompt": "this is a valid test prompt",
            }
        )
        result = validate_request(encoded_data)
        self.assertEqual(result, None)

    def test_validate_request_missing_prompt(self):
        encoded_data = PromptForm(
            {
                "p_type": "parse",
            }
        )
        result = validate_request(encoded_data)
        json = JsonResponse({"prompt": ["This field is required."]}, status=400)
        self.assertEqual(result.content, json.content)  # type: ignore

    def test_validate_request_missing_p_type(self):
        encoded_data = PromptForm(
            {
                "prompt": "this is a valid test prompt",
            }
        )
        result = validate_request(encoded_data)
        json = JsonResponse({"p_type": ["This field is required."]}, status=400)
        self.assertEqual(result.content, json.content)  # type: ignore

    def test_validate_request_unknown_p_type(self):
        encoded_data = PromptForm(
            {
                "prompt": "this is a valid test prompt",
                "p_type": "unknown",
            }
        )
        result = validate_request(encoded_data)
        json = JsonResponse(
            {
                "p_type": [
                    "Select a valid choice. unknown is not one of the available choices."
                ]
            },
            status=400,
        )
        self.assertEqual(result.content, json.content)  # type: ignore

    def test_validate_request_empty_prompt(self):
        encoded_data = PromptForm(
            {
                "prompt": "",
                "p_type": "parse",
            }
        )
        result = validate_request(encoded_data)
        json = JsonResponse({"prompt": ["This field is required."]}, status=400)
        self.assertEqual(result.content, json.content)  # type: ignore

    def test_validate_request_empty_p_type(self):
        encoded_data = PromptForm(
            {
                "prompt": "this is a valid test prompt",
                "p_type": "",
            }
        )
        result = validate_request(encoded_data)
        json = JsonResponse({"p_type": ["This field is required."]}, status=400)
        self.assertEqual(result.content, json.content)  # type: ignore

    def test_validate_request_empty_parameters(self):
        encoded_data = PromptForm({})
        result = validate_request(encoded_data)
        json = JsonResponse(
            {
                "prompt": ["This field is required."],
                "p_type": ["This field is required."],
            },
            status=400,
        )
        self.assertEqual(result.content, json.content)  # type: ignore

    @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.messages.create")
    @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.runs.create")
    def test_handle_run_creation_valid(self, mock_runs_create, mock_messages_create):
        mock_runs_create.return_value = MockRun("run_id")
        mock_messages_create.return_value = "Message created"
        p_type = "parse"
        prompt = "this is a valid test prompt"
        result = handle_run_creation(p_type, prompt)
        self.assertEqual(result, "run_id")

    @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.messages.create")
    @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.runs.create")
    def test_handle_run_creation_invalid_type(
        self, mock_runs_create, mock_messages_create
    ):
        mock_runs_create.return_value = MockRun("run_id")
        mock_messages_create.return_value = "Message created"
        p_type = "unknown"
        prompt = "this is a valid test prompt"
        with self.assertRaises(ValueError):
            handle_run_creation(p_type, prompt)

    @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.messages.create")
    @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.runs.create")
    def test_handle_run_creation_empty_prompt(
        self, mock_runs_create, mock_messages_create
    ):
        mock_runs_create.return_value = MockRun("run_id")
        mock_messages_create.return_value = "Message created"
        p_type = "unknown"
        prompt = "this is a valid test prompt"
        with self.assertRaises(ValueError):
            handle_run_creation(p_type, prompt)

    @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.messages.create")
    @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.runs.create")
    def test_handle_run_creation_create_message_error(
        self, mock_runs_create, mock_messages_create
    ):
        mock_runs_create.return_value = MockRun("run_id")
        mock_messages_create.side_effect = ValueError("An error occurred")
        p_type = "unknown"
        prompt = "this is a valid test prompt"
        with self.assertRaises(ValueError):
            handle_run_creation(p_type, prompt)

    @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.messages.create")
    @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.runs.create")
    def test_handle_run_creation_create_run_error(
        self, mock_runs_create, mock_messages_create
    ):
        mock_runs_create.return_value = MockRun("run_id")
        mock_messages_create.side_effect = ValueError("An error occurred")
        p_type = "unknown"
        prompt = "this is a valid test prompt"
        with self.assertRaises(ValueError):
            handle_run_creation(p_type, prompt)
