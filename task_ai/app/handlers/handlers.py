from django.http import HttpResponse, JsonResponse
from .helpers import (
    PromptType,
    validate_prompt_request,
    extract_prompt_request_data,
    handle_run_creation,
    client,
    PARSING_THREAD_ID,
    CAT_THREAD_ID
)



def list_messages(request):
    asst_type = request.query_params.get("assistant", "")
    message_list = []

    if asst_type == PromptType.PARSE.value:
        message_list = client.beta.threads.messages.list(
            thread_id=PARSING_THREAD_ID
        ).json()

    elif asst_type == PromptType.CAT.value:
        message_list = client.beta.threads.messages.list(thread_id=CAT_THREAD_ID).json()

    return HttpResponse(
        message_list,
        content_type="application/json",
    )

def send_prompt(request):
    validation_result = validate_prompt_request(request)

    prompt, p_type = extract_prompt_request_data(request)

    if validation_result:
        return validation_result

    run = handle_run_creation(p_type, prompt)

    return JsonResponse(data={"run_id": run.id})


# TODO: Make this a Celery task that calls a webhook once the run is done
def get_run_status(request):
    thread_id = ""

    run_id = request.query_params.get("run_id", "")
    p_type = request.query_params.get("type", "")

    if p_type == PromptType.PARSE.value:
        thread_id = PARSING_THREAD_ID
    elif p_type == PromptType.CAT.value:
        thread_id = CAT_THREAD_ID

    run = client.beta.threads.runs.retrieve(run_id, thread_id=thread_id)

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id).json()
        return HttpResponse(messages, content_type="application/json")

    return HttpResponse(status=run.status, content_type="application/json")
