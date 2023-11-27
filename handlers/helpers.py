import logging
from enum import Enum
import os
from typing import Optional
from django import forms
from django.http import JsonResponse
from dotenv import load_dotenv
from openai import OpenAI


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




client = OpenAI(api_key=API_KEY)


