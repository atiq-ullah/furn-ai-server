import os
import time
import logging

from django.http import JsonResponse, HttpRequest
from dotenv import load_dotenv
from celery import Celery

from .helpers import (
    PromptForm,
    MessageForm,
    validate_request,
    promptTypeMap,
    client,
    handle_run_creation,
)

from .setup_signals import SignalConnection

# TODO: env variable for Rabbitmq connection
# TODO: env variable for timeout

conn = SignalConnection()
established_conn = conn.connect_to_rabbitmq("guest", "guest")
parse_channel = conn.setup_channel(established_conn, "prompt", "prompt_parse", "parse")
cat_channel = conn.setup_channel(established_conn, "prompt", "prompt_cat", "cat")


load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_ai.settings")
debug = os.getenv("DEBUG")
address = "localhost" if debug == 1 else "rabbitmq"

app = Celery(
    "handlers",
    broker_connection_retry_on_startup=True,
    broker="amqp://guest:guest@" + address + ":5672//",
)
app.config_from_object("django.conf:settings", namespace="CELERY")


logger = logging.getLogger(__name__)


def post_prompt_handler(request: HttpRequest):
    form = PromptForm(request.POST)
    logger.info("Form: %s", form)
    validation = validate_request(form)
    logger.info(validation)

    if validation:
        return validation

    prompt = form.cleaned_data["prompt"]
    p_type = form.cleaned_data["p_type"]

    logger.info("Prompt: %s", prompt)
    logger.info("Prompt type: %s", p_type)
    try:
        run_id = handle_run_creation(p_type, prompt)
        periodically_check_run_status.delay(p_type, run_id)
    except Exception as e:  # pylint: disable=broad-except
        logger.error("An error occurred: %s", e)
        return JsonResponse(data={"error": str(e)}, status=500)

    return JsonResponse(data={"run_id": run_id})


def get_prompt_handler(request: HttpRequest):
    form = MessageForm(request.GET)
    logger.info("Form: %s", form)
    validation = validate_request(form)
    logger.info(validation)

    if validation:
        return validation

    p_type = form.cleaned_data["p_type"]

    if p_type not in promptTypeMap:
        return JsonResponse(
            data={"error": f"Prompt type {p_type} is not supported"}, status=400
        )

    message_list = client.beta.threads.messages.list(
        thread_id=promptTypeMap[p_type]  # type: ignore
    ).json()  # type: ignore

    return JsonResponse(data=message_list)


@app.task(soft_time_limit=30)  # type: ignore
def periodically_check_run_status(p_type: str, run_id: str):
    while True:
        try:
            time.sleep(2)
            run = client.beta.threads.runs.retrieve(
                run_id, thread_id=promptTypeMap[p_type]  # type: ignore
            )

            if run.status == "completed":
                last_message = (
                    client.beta.threads.messages.list(thread_id=promptTypeMap[p_type])  # type: ignore
                    .data[0]
                    .content[0]
                )
                print(last_message.text.value)  # type: ignore
                if p_type == "parse":
                    parse_channel.basic_publish(  # type: ignore
                        exchange="prompt",
                        routing_key="parse",
                        body=last_message.text.value,  # type: ignore
                    )
                else:
                    cat_channel.basic_publish(  # type: ignore
                        exchange="prompt",
                        routing_key="cat",
                        body=last_message.text.value,  # type: ignore
                    )  # TODO: Signal another function here to send response on socket
                break
        except Exception as e:  # pylint: disable=broad-except
            logger.error("An error occurred: %s", e)
