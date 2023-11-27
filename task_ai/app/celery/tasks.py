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