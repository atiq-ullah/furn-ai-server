from enum import Enum
import json
import os
from django.http import JsonResponse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class PromptType(Enum):
    PARSE = "parse"
    CAT = "cat"


PARSING_ASST_ID = os.environ.get("OPENAI_PARSING_ASST_ID")
PARSING_THREAD_ID = os.environ.get("OPENAI_PARSING_THREAD_ID")

CAT_ASST_ID = os.environ.get("OPENAI_CATEGORIZING_ASST_ID")
CAT_THREAD_ID = os.environ.get("OPENAI_CATEGORIZING_THREAD_ID")
MODEL = os.environ.get("OPENAI_MODEL")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def extract_prompt_request_data(request):
    data = json.loads(request.body)

    prompt = data.get("prompt", "")
    p_type = data.get("type", PromptType.PARSE.value)

    return prompt, p_type


def validate_prompt_request(request):
    method = request.method
    prompt, p_type = extract_prompt_request_data(request)

    if method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    if prompt == "":
        return JsonResponse({"error": "Prompt cannot be empty"}, status=400)
    if p_type not in PromptType:
        return JsonResponse({"error": "Invalid prompt type"}, status=400)

    return None


def handle_run_creation(p_type, prompt):
    if p_type == PromptType.PARSE.value:
        client.beta.threads.messages.create(
            thread_id=PARSING_THREAD_ID, role="user", content=prompt
        )
        return client.beta.threads.runs.create(
            thread_id=PARSING_THREAD_ID, assistant_id=PARSING_ASST_ID
        )
    elif p_type == PromptType.CAT.value:
        client.beta.threads.messages.create(
            thread_id=CAT_THREAD_ID, role="user", content=prompt
        )
        return client.beta.threads.runs.create(
            thread_id=CAT_THREAD_ID, assistant_id=PARSING_ASST_ID
        )
