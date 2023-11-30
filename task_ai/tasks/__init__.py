import os
from task_ai.openai_client import PromptType, get_last_message, get_run_status
from task_ai.celery import app
from task_ai.signals import setup_mq_connections


REQUEST_INTERVAL = os.environ.get("OPENAI_REQUEST_INTERVAL", 5)


@app.task(bind=True)
def monitor_run_status(self, p_type, run_id):
    status = get_run_status(PromptType(p_type), run_id)

    if status == "completed":
        last_message = get_last_message(PromptType(p_type))
        handle_response.delay(p_type, last_message)
        return last_message

    self.apply_async(countdown=5, args=[p_type, run_id])
    return status


@app.task(bind=True)
def handle_response(self, p_type, message):  # pylint: disable=unused-argument
    print("Message in handle response: \n" + message)
    channel = setup_mq_connections(
        exchange_name="openai", queue_name="openai", routing_key="openai"
    )
    if channel is None:
        return None
    channel.basic_publish(exchange="openai", routing_key="openai", body=message)
    return message
