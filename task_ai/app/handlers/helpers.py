import logging
from enum import Enum
import os
from django import forms
from django.http import JsonResponse
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional


load_dotenv()

PARSING_ASST_ID = os.environ.get("OPENAI_PARSING_ASST_ID")
PARSING_THREAD_ID = os.environ.get("OPENAI_PARSING_THREAD_ID")

CAT_ASST_ID = os.environ.get("OPENAI_CATEGORIZING_ASST_ID")
CAT_THREAD_ID = os.environ.get("OPENAI_CATEGORIZING_THREAD_ID")
MODEL = os.environ.get("OPENAI_MODEL")
API_KEY = os.environ.get("OPENAI_API_KEY")


promptTypeMap = {"parse": PARSING_THREAD_ID, "cat": CAT_THREAD_ID}

asstTypeMap = {"parse": PARSING_ASST_ID, "cat": CAT_ASST_ID}


class PromptType(Enum):
    PARSE = "parse"
    CAT = "cat"


logger = logging.getLogger(__name__)


class PromptForm(forms.Form):
    prompt = forms.CharField(required=True)
    p_type = forms.ChoiceField(
        choices=[("parse", "Parse"), ("cat", "Cat")], required=True
    )


class MessageForm(forms.Form):
    p_type = forms.ChoiceField(
        choices=[("parse", "Parse"), ("cat", "Cat")], required=True
    )


client = OpenAI(api_key=API_KEY)


def validate_request(form: forms.Form) -> Optional[JsonResponse]:
    if form.is_valid():
        return None
    else:
        return JsonResponse(form.errors, status=400)


def handle_run_creation(p_type: str, prompt: str) -> str:
    thread_id = promptTypeMap.get(p_type)
    assistant_id = asstTypeMap.get(p_type)

    if thread_id is None or assistant_id is None:
        raise ValueError(f"Invalid prompt type: {p_type}")

    try:
        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id
        )
    except Exception as e:
        logger.error(e)
        raise e

    return run.id
