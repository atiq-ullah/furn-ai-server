from os import environ
from dotenv import load_dotenv
from openai import OpenAI
from enum import Enum
load_dotenv()

# OpenAI
PARSING_ASST_ID = environ.get("OPENAI_PARSING_ASST_ID")
PARSING_THREAD_ID = environ.get("OPENAI_PARSING_THREAD_ID")

CAT_ASST_ID = environ.get("OPENAI_CATEGORIZING_ASST_ID")
CAT_THREAD_ID = environ.get("OPENAI_CATEGORIZING_THREAD_ID")

MODEL = environ.get("OPENAI_MODEL")
API_KEY = environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

promptTypeMap = {"parse": PARSING_THREAD_ID, "cat": CAT_THREAD_ID}
asstTypeMap = {"parse": PARSING_ASST_ID, "cat": CAT_ASST_ID}
class PromptType(Enum):
    PARSE = "parse"
    CAT = "cat"

def get_ids():
    return PARSING_ASST_ID, PARSING_THREAD_ID, CAT_ASST_ID, CAT_THREAD_ID
    