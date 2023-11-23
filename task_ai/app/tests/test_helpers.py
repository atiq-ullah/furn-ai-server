from django import forms
from django.test import TestCase, RequestFactory
from django.http import JsonResponse

import requests
from urllib.parse import urlencode

from task_ai.app.handlers.helpers import (
    validate_request,
    PromptForm,
)

class InputForm(forms.Form):
    prompt = forms.CharField(required=False)
    p_type = forms.CharField(required=False)



# Create a form instance with the data
# form = MyForm(data)
class HelpersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_validate_request_valid(self):
        encoded_data = PromptForm({
            'p_type': 'parse',
            'prompt': 'this is a valid test prompt',
        })
        result = validate_request(encoded_data)
        self.assertEqual(result, None)

    def test_validate_request_missing_prompt(self):
        encoded_data = PromptForm({
            'p_type': 'parse',
        })
        result = validate_request(encoded_data)
        json = JsonResponse({'prompt': ['This field is required.']}, status=400)
        self.assertEqual(result.content, json.content)


    def test_validate_request_missing_p_type(self):
        encoded_data = PromptForm({
            'prompt': 'this is a valid test prompt',
        })
        result = validate_request(encoded_data)
        json = JsonResponse({'p_type': ['This field is required.']}, status=400)
        self.assertEqual(result.content, json.content)

    def test_validate_request_unknown_p_type(self):
        encoded_data = PromptForm({
            'prompt': 'this is a valid test prompt',
            'p_type': 'unknown',
        })
        result = validate_request(encoded_data)
        json = JsonResponse({"p_type": ["Select a valid choice. unknown is not one of the available choices."]}, status=400)
        self.assertEqual(result.content, json.content)

    def test_validate_request_empty_prompt(self):
        encoded_data = PromptForm({
            'prompt': '',
            'p_type': 'parse',
        })
        result = validate_request(encoded_data)
        json = JsonResponse({'prompt': ['This field is required.']}, status=400)
        self.assertEqual(result.content, json.content)

    def test_validate_request_empty_p_type(self):
        encoded_data = PromptForm({
            'prompt': 'this is a valid test prompt',
            'p_type': '',
        })
        result = validate_request(encoded_data)
        json = JsonResponse({"p_type": ["This field is required."]}, status=400)
        self.assertEqual(result.content, json.content)

    def test_validate_request_empty_parameters(self):
        encoded_data = PromptForm({})
        result = validate_request(encoded_data)
        json = JsonResponse({"prompt": ["This field is required."], "p_type": ["This field is required."]}, status=400)
        self.assertEqual(result.content, json.content)

    # @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.messages.create")
    # @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.runs.create")   
    def test_handle_run_creation_valid(self):
        pass

    def test_handle_run_creation_invalid_type(self):
        pass

    def test_handle_run_creation_empty_prompt(self):
        pass

    def test_handle_run_creation_create_message_error(self):
        pass

    def test_handle_run_creation_create_run_error(self):
        pass
    # def test_extract_prompt_request_data(self):
    #     request = self.factory.post(
    #         "/prompt/",
    #         '{"prompt": "test prompt", "p_type": "parse"}',
    #         content_type="application/json",
    #     )
    #     result = extract_prompt_request_data(request)
    #     self.assertEqual(result, ("test prompt", "parse"))

    # def test_extract_prompt_request_type_default(self):
    #     request = self.factory.post(
    #         "/prompt/", '{"prompt": "test prompt"}', content_type="application/json"
    #     )
    #     result = extract_prompt_request_data(request)
    #     self.assertEqual(result, ("test prompt", "parse"))

    # def test_validate_prompt_request(self):
    #     request = self.factory.post(
    #         "/prompt/",
    #         '{"prompt": "test prompt", "p_type": "cat"}',
    #         content_type="application/json",
    #     )
    #     result = validate_prompt_request(request)
    #     self.assertEqual(result, None)

    # def test_validate_prompt_request_invalid_method(self):
    #     request = self.factory.delete(
    #         "/prompt/",
    #         '{"prompt": "test prompt", "p_type": "cat"}',
    #         content_type="application/json",
    #     )
    #     result = validate_prompt_request(request)
    #     self.assertEqual(result.status_code, 400)
    #     self.assertEqual(
    #         json.loads(result.content), {"error": "Invalid request method"}
    #     )

    # def test_validate_prompt_request_empty_prompt(self):
    #     request = self.factory.post(
    #         "/prompt/",
    #         '{"prompt": "", "p_type": "parse"}',
    #         content_type="application/json",
    #     )
    #     result = validate_prompt_request(request)
    #     self.assertEqual(result.status_code, 400)
    #     self.assertEqual(
    #         json.loads(result.content), {"error": "Prompt cannot be empty"}
    #     )

    # def test_validate_prompt_request_invalid_type(self):
    #     request = self.factory.post(
    #         "/prompt/",
    #         '{"prompt": "non empty", "p_type": "unknown"}',
    #         content_type="application/json",
    #     )
    #     result = validate_prompt_request(request)
    #     self.assertEqual(result.status_code, 400)
    #     self.assertEqual(json.loads(result.content), {"error": "Invalid prompt type"})

    # @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.messages.create")
    # @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.runs.create")
    # def test_handle_run_creation(self, mock_runs_create, mock_messages_create):
    #     mock_runs_create.return_value = "Run created"
    #     mock_messages_create.return_value = "Message created"

    #     result = handle_run_creation(PromptType.PARSE.value, "test prompt")
    #     mock_messages_create.assert_called_once_with(
    #         thread_id=PARSING_THREAD_ID, role="user", content="test prompt"
    #     )
    #     mock_runs_create.assert_called_once_with(
    #         thread_id=PARSING_THREAD_ID, assistant_id=PARSING_ASST_ID
    #     )
    #     self.assertEqual(result, "Run created")

    #     mock_messages_create.reset_mock()
    #     mock_runs_create.reset_mock()

    #     result = handle_run_creation(PromptType.CAT.value, "test prompt")
    #     mock_messages_create.assert_called_once_with(
    #         thread_id=CAT_THREAD_ID, role="user", content="test prompt"
    #     )
    #     mock_runs_create.assert_called_once_with(
    #         thread_id=CAT_THREAD_ID, assistant_id=CAT_ASST_ID
    #     )
    #     self.assertEqual(result, "Run created")

    # @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.messages.create")
    # @mock.patch("task_ai.app.handlers.helpers.client.beta.threads.runs.create")
    # def test_create_run(self, mock_runs_create, mock_messages_create):
    #     mock_runs_create.return_value = "Run created"
    #     mock_messages_create.return_value = "Message created"

    #     assistant_id = "assistant_id"
    #     thread_id = "thread_id"
    #     prompt = "test prompt"

    #     result = create_run(assistant_id, thread_id, prompt)

    #     mock_messages_create.assert_called_once_with(
    #         thread_id=thread_id, role="user", content=prompt
    #     )
    #     mock_runs_create.assert_called_once_with(
    #         thread_id=thread_id, assistant_id=assistant_id
    #     )
    #     self.assertEqual(result, "Run created")
