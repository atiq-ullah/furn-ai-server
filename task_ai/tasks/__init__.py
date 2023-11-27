
from task_ai.openai_client.client import (
    PromptType,
    get_last_message,
    get_run_status
)
from task_ai.celery import app

@app.task(bind=True)
def monitor_run_status(self, p_type, run_id):
    status = get_run_status(PromptType(p_type), run_id)

    if status == "completed":
        last_message = get_last_message(PromptType(p_type))
        handle_response.delay(p_type, last_message)
        return last_message
    else:
        self.apply_async(countdown=5, args=[p_type, run_id])

@app.task(bind=True)
def handle_response(self, p_type, message):
    print("Message in handle response: \n" + message)