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
def send_run_creation(p_type, prompt):
    run = handle_run_creation(p_type, prompt)
    periodically_check_run_status.delay(p_type, run.id)
    return run.id
    
def send_prompt(request):
    validation_result = validate_prompt_request(request)

    prompt, p_type = extract_prompt_request_data(request)

    if validation_result:
        return validation_result
    
    run_id = send_run_creation(p_type, prompt)


    
    return JsonResponse(data={"run_id": run_id})

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
def periodically_check_run_status(p_type, run_id):
    thread_id = ""

    if p_type == PromptType.PARSE.value:
        thread_id = PARSING_THREAD_ID
    elif p_type == PromptType.CAT.value:
        thread_id = CAT_THREAD_ID

    while True:
        try:
            time.sleep(5)
            run = client.beta.threads.runs.retrieve(run_id, thread_id=thread_id)   

            if run.status == "completed":
                last_message = client.beta.threads.messages.list(thread_id=thread_id).data[0].content[0]
                print(last_message.text.value)
                break
            else:
                print(f'Run status: {run.status}')


        except Exception as e:
            print(f'An error occurred: {e}')
