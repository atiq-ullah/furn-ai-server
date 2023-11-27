import os
import time
import logging
from tkinter import E
from task_ai.app.openai_client import (
    get_last_message,
    get_message_list,
    add_message_to_thread,
    start_run_on_thread,
    get_run_status,
)

from django.http import JsonResponse, HttpRequest
from dotenv import load_dotenv
from celery import Celery


from .setup_signals import SignalConnection

# TODO: env variable for Rabbitmq connection
# TODO: env variable for timeout

conn = SignalConnection()
# TODO: Better credentials here
established_conn = conn.connect_to_rabbitmq("guest", "guest")
# TODO: Use a single queue here with different routing keys
parse_channel = conn.setup_channel(established_conn, "prompt", "prompt_parse", "parse")
cat_channel = conn.setup_channel(established_conn, "prompt", "prompt_cat", "cat")

# TODO: Do I need to always load dotenv?
load_dotenv()

# TODO: There is a better place for these for sure
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_ai.settings")
address = os.environ.get("RABBITMQ_ADDRESS")
address = "localhost" if address is None else address
app = Celery(
    "handlers",
    broker_connection_retry_on_startup=True,
    broker="amqp://guest:guest@" + address + ":5672//",
    broker_connection_retry=True,
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
    
    message_return = add_message()
    run_id = start_run()
    periodically_check_run_status()

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

# TODO: Move this to a different file
@app.task(soft_time_limit=30)  # type: ignore
def periodically_check_run_status(p_type: str, run_id: str):
    while True:
        time.sleep(5)

        try:
            run = client.beta.threads.runs.retrieve(
                run_id, thread_id=promptTypeMap[p_type]  # type: ignore
            )

        except Exception as e:  # pylint: disable=broad-except
            logger.error("Unable to retrieve run: %s", e)
            return

        if run.status == "completed":
            last_message = (
                client.beta.threads.messages.list(thread_id=promptTypeMap[p_type])  # type: ignore
                .data[0]
                .content[0]
            )

            if p_type == "parse":
                try:
                    parse_channel.basic_publish(  # type: ignore
                        exchange="prompt",
                        routing_key="parse",
                        body=last_message.text.value,  # type: ignore
                    )
                    return
                except Exception as e:  # pylint: disable=broad-except
                    logger.error("Unable to send parse: %s", e)
                    return

            else:
                try:
                    cat_channel.basic_publish(  # type: ignore
                        exchange="prompt",
                        routing_key="cat",
                        body=last_message.text.value,  # type: ignore
                    )  # TODO: Signal another function here to send response on socket
                    return
                except Exception as e:  # pylint: disable=broad-except
                    logger.error("Unable to send cat: %s", e)
                    break
