import logging
from enum import Enum
import os
from typing import Optional
from django import forms
from django.http import JsonResponse


logger = logging.getLogger(__name__)

from .types import *
from .constants import *


def validate_request(form: forms.Form) -> Optional[JsonResponse]:
    if form.is_valid():
        return None
    return JsonResponse(form.errors, status=400)


# TODO: Better error handling here
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
