import os
from queue import Queue

import boto3

from app.models import NetworkEvent


# Local queue for development and automated tests.
event_queue: Queue[NetworkEvent] = Queue()

# Select the queue backend through an environment variable.
QUEUE_BACKEND = os.getenv("QUEUE_BACKEND", "local").lower()

# AWS SQS configuration.
AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
AWS_SQS_QUEUE_URL = os.getenv("AWS_SQS_QUEUE_URL")


def enqueue_event(event: NetworkEvent) -> None:
    """Send a validated event to the selected queue."""

    if QUEUE_BACKEND == "local":
        event_queue.put(event)

    elif QUEUE_BACKEND == "sqs":
        if not AWS_SQS_QUEUE_URL:
            raise ValueError("AWS_SQS_QUEUE_URL is not configured.")

        sqs = boto3.client("sqs", region_name=AWS_REGION)

        sqs.send_message(
            QueueUrl=AWS_SQS_QUEUE_URL,
            MessageBody=event.model_dump_json(),
        )

    else:
        raise ValueError(
            f"Unsupported queue backend: {QUEUE_BACKEND}"
        )


def dequeue_event() -> NetworkEvent:
    """Retrieve the next event from the local queue."""
    return event_queue.get()
