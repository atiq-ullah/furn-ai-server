from enum import Enum
import json
import os
from django.http import JsonResponse
from django import forms
from openai import OpenAI
import logging
from dotenv import load_dotenv

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
    run_id = forms.CharField(required=True)
    p_type = forms.ChoiceField(
        choices=[("parse", "Parse"), ("cat", "Cat")], required=True
    )


client = OpenAI(api_key=API_KEY)


def validate_request(form):
    if form.is_valid():
        return None
    else:
        return JsonResponse(form.errors, status=400)


def send_run_creation(p_type, prompt):
    run = handle_run_creation(p_type, prompt)
    return run.id


def handle_run_creation(p_type, prompt):
    client.beta.threads.messages.create(
        thread_id=promptTypeMap[p_type], role="user", content=prompt
    )

    return client.beta.threads.runs.create(
        thread_id=promptTypeMap[p_type], assistant_id=asstTypeMap[p_type]
    )
