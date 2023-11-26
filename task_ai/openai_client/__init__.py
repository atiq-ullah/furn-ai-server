from os import environ
from enum import Enum
from typing import Optional
import logging
from openai import OpenAI
from django.forms import CharField, ChoiceField, Form
from django.http import HttpRequest, JsonResponse

from dotenv import load_dotenv

load_dotenv()

# OpenAI
PARSING_ASST_ID = environ.get("OPENAI_PARSING_ASST_ID") or ""
PARSING_THREAD_ID = environ.get("OPENAI_PARSING_THREAD_ID") or ""

CAT_ASST_ID = environ.get("OPENAI_CATEGORIZING_ASST_ID")
CAT_THREAD_ID = environ.get("OPENAI_CATEGORIZING_THREAD_ID")

MODEL = environ.get("OPENAI_MODEL")
API_KEY = environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

logger = logging.getLogger(__name__)


type_to_thread_id = {"parse": PARSING_THREAD_ID, "cat": CAT_THREAD_ID}
type_to_assistant_id = {"parse": PARSING_ASST_ID, "cat": CAT_ASST_ID}


class PromptForm(Form):
    prompt = CharField(required=True)
    p_type = ChoiceField(choices=[("parse", "Parse"), ("cat", "Cat")], required=True)


class MessageForm(Form):
    p_type = ChoiceField(choices=[("parse", "Parse"), ("cat", "Cat")], required=True)


class PromptType(Enum):
    PARSE = "parse"
    CAT = "cat"


def validate_request(request: HttpRequest) -> Optional[JsonResponse]:
    form = None
    if request.method == "POST":
        form = PromptForm(request.POST)
    elif request.method == "GET":
        form = MessageForm(request.GET)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

    if form is not None:
        if form.is_valid():
            return None
        return JsonResponse(form.errors, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_last_message(p_type: PromptType) -> str:
    logger.info("Retrieving last message from thread: %s", p_type.value)
    try:
        message_list = client.beta.threads.messages.list(
            thread_id=type_to_thread_id[p_type.value]
        )
    except Exception as e:
        logger.error("Could not retrieve last message from thread: %s", e)
        raise e
    last_message = message_list.data[0]
    if last_message.content[0].type == "text":
        return last_message.content[0].text.value
    return ""


def get_message_list(p_type: PromptType) -> str:
    logger.info("Retrieving messages from thread: %s", p_type.value)
    try:
        message_list = client.beta.threads.messages.list(
            thread_id=type_to_thread_id[p_type.value]
        )
    except Exception as e:
        logger.error("Could not retrieve messages from thread: %s", e)
        raise e
    return message_list.model_dump_json()


def add_message_to_thread(p_type: PromptType, message: str) -> str:
    logger.info("Adding messages: %s to thread: %s", message, p_type.value)
    thread_id = type_to_thread_id[p_type.value]
    try:
        thread_message = client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=message
        )
    except Exception as e:
        logger.error("Could not add message to thread: %s", e)
        raise e
    return thread_message.id


def start_run_on_thread(p_type: PromptType) -> str:
    logger.info("Starting run on thread: %s", p_type.value)
    thread_id = type_to_thread_id[p_type.value]
    assistant_id = type_to_assistant_id[p_type.value]
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id
        )
    except Exception as e:
        logger.error("Could not start run on thread: %s", e)
        raise e
    return run.id


def get_run_status(p_type: PromptType, run_id: str):
    try:
        run = client.beta.threads.runs.retrieve(
            thread_id=type_to_thread_id[p_type.value], run_id=run_id
        )
    except Exception as e:
        logger.error("Could not start run on thread: %s", e)
        raise e
    return run.status
