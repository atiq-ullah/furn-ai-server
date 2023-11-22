from django.test import TestCase, RequestFactory

from task_ai.app.handlers.helpers import (
    validate_request,
    PromptForm,
)


class HelpersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    def test_validate_request_post_valid(self):
        request = self.factory.post(
            "/prompt",
            '{"prompt": "test prompt", "p_type": "parse"}',
            content_type="application/json",
        )
        form = PromptForm(request.POST)
        result = validate_request(form)
        self.assertEqual(result, None)

    def test_validate_request_post_invalid(self):
        pass

    def test_validate_request_get_valid(self):
        pass

    def test_validate_request_get_invalid(self):
        pass

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
