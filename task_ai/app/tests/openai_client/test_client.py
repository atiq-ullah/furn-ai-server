import unittest
from unittest.mock import patch, MagicMock
from task_ai.app.openai_client.client import (
    validate_request,
    get_last_message,
    get_message_list,
    add_message_to_thread,
    start_run_on_thread,
    get_run_status,
    PromptType,
    PromptForm
)
from django.http import JsonResponse

class TestYourModuleName(unittest.TestCase):

    def setUp(self):
        self.mock_openai_client = MagicMock()

    # Test validate_request function
    def test_validate_request_valid(self):
        form = PromptForm(data={'prompt': 'Example prompt', 'p_type': 'parse'})
        self.assertIsNone(validate_request(form))

    def test_validate_request_invalid(self):
        form = PromptForm(data={})
        response = validate_request(form)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)

    # Test get_last_message function
    @patch('your_module_name.client', new_callable=lambda: self.mock_openai_client)
    def test_get_last_message_success(self, mock_client):
        mock_client.beta.threads.messages.list.return_value.data = [
            MagicMock(content=[MagicMock(type="text", text=MagicMock(value="Test message"))])
        ]
        result = get_last_message(PromptType.PARSE)
        self.assertEqual(result, "Test message")

    @patch('your_module_name.client', new_callable=lambda: self.mock_openai_client)
    def test_get_last_message_failure(self, mock_client):
        mock_client.beta.threads.messages.list.side_effect = Exception("Error")
        with self.assertRaises(Exception):
            get_last_message(PromptType.PARSE)

    # Test get_message_list function
    @patch('your_module_name.client', new_callable=lambda: self.mock_openai_client)
    def test_get_message_list_success(self, mock_client):
        mock_client.beta.threads.messages.list.return_value.model_dump_json.return_value = "message list json"
        result = get_message_list(PromptType.PARSE)
        self.assertEqual(result, "message list json")

    @patch('your_module_name.client', new_callable=lambda: self.mock_openai_client)
    def test_get_message_list_failure(self, mock_client):
        mock_client.beta.threads.messages.list.side_effect = Exception("Error")
        with self.assertRaises(Exception):
            get_message_list(PromptType.PARSE)

    # Test add_message_to_thread function
    @patch('your_module_name.client', new_callable=lambda: self.mock_openai_client)
    def test_add_message_to_thread_success(self, mock_client):
        mock_client.beta.threads.messages.create.return_value.id = "123"
        result = add_message_to_thread(PromptType.PARSE, "Test message")
        self.assertEqual(result, "123")

    @patch('your_module_name.client', new_callable=lambda: self.mock_openai_client)
    def test_add_message_to_thread_failure(self, mock_client):
        mock_client.beta.threads.messages.create.side_effect = Exception("Error")
        with self.assertRaises(Exception):
            add_message_to_thread(PromptType.PARSE, "Test message")

    # Test start_run_on_thread function
    @patch('your_module_name.client', new_callable=lambda: self.mock_openai_client)
    def test_start_run_on_thread_success(self, mock_client):
        mock_client.beta.threads.runs.create.return_value.id = "run123"
        result = start_run_on_thread(PromptType.PARSE)
        self.assertEqual(result, "run123")

    @patch('your_module_name.client', new_callable=lambda: self.mock_openai_client)
    def test_start_run_on_thread_failure(self, mock_client):
        mock_client.beta.threads.runs.create.side_effect = Exception("Error")
        with self.assertRaises(Exception):
            start_run_on_thread(PromptType.PARSE)

    # Test get_run_status function
    @patch('your_module_name.client', new_callable=lambda: self.mock_openai_client)
    def test_get_run_status_success(self, mock_client):
        mock_client.beta.threads.runs.retrieve.return_value.status = "completed"
        result = get_run_status(PromptType.PARSE, "run123")
        self.assertEqual(result, "completed")

    @patch('your_module_name.client', new_callable=lambda: self.mock_openai_client)
    def test_get_run_status_failure(self, mock_client):
        mock_client.beta.threads.runs.retrieve.side_effect = Exception("Error")
        with self.assertRaises(Exception):
            get_run_status(PromptType.PARSE, "run123")

if __name__ == '__main__':
    unittest.main()
