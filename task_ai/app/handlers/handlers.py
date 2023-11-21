import json
import time
from django.http import JsonResponse
from .helpers import (
    PromptType,
    validate_prompt_request,
    extract_prompt_request_data,
    handle_run_creation,
    client,
    PARSING_THREAD_ID,
    CAT_THREAD_ID
)
from . import celery


# from task_ai.app.tasks import check_run_status
def list_messages(request):
    asst_type = request.GET.get("assistant", "")
    message_list = []

    if asst_type == PromptType.PARSE.value:
        message_list = client.beta.threads.messages.list(
            thread_id=PARSING_THREAD_ID
        ).json()

    elif asst_type == PromptType.CAT.value:
        message_list = client.beta.threads.messages.list(
            thread_id=CAT_THREAD_ID).json()

    return JsonResponse({"message": message_list})

def send_prompt(request):
    validation_result = validate_prompt_request(request)

    prompt, p_type = extract_prompt_request_data(request)

    if validation_result:
        return validation_result

    run = handle_run_creation(p_type, prompt)
    celery_get_run_status.delay(p_type, run.id)
    


    return JsonResponse(data={"run_id": run.id})


# TODO: Make this a Celery task that calls a webhook once the run is done
def get_run_status(request):
    thread_id = ""

    run_id = request.GET.get("run_id", "")
    p_type = request.GET.get("p_type", "")

    if p_type == PromptType.PARSE.value:
        thread_id = PARSING_THREAD_ID
    elif p_type == PromptType.CAT.value:
        thread_id = CAT_THREAD_ID

    run = client.beta.threads.runs.retrieve(run_id, thread_id=thread_id)

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id).json()
        return JsonResponse({ "messages": messages })

    return JsonResponse({"status": run.status})

@celery.task(soft_time_limit=30)
def celery_get_run_status(p_type, run_id):
    thread_id = ""

    if p_type == PromptType.PARSE.value:
        thread_id = PARSING_THREAD_ID
    elif p_type == PromptType.CAT.value:
        thread_id = CAT_THREAD_ID
    
    run = client.beta.threads.runs.retrieve(run_id, thread_id=thread_id)
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id).json()
        return messages

    print("run status: ", run.status)

    while True:
        run = client.beta.threads.runs.retrieve(run_id, thread_id=thread_id)   
        print("run status: ", run.status)
 
        time.sleep(1)

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id).json()
            # Feed the result into another prompt call
            # Re-use the send_prompt and this task
            # Need to handle if the type is cat and it has completed since that means
            # We need to send the result to the Django channel for the client
            print("message", messages)
            return run.status

    print("run status: ", run.status)
    return run.status