import os

import boto3

from app.alerts import create_alert
from app.detection import detect_incident
from app.event_queue import dequeue_event, event_queue
from app.models import NetworkEvent
from app.storage import save_record


AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
AWS_SQS_QUEUE_URL = os.getenv("AWS_SQS_QUEUE_URL")


def process_event(event: NetworkEvent) -> dict:
    """Process a validated event and return its detection result."""

    result = detect_incident(event)

    return {
        "event_id": event.event_id,
        "processing_status": "processed",
        "incident": result,
    }


def process_next_event() -> dict | None:
    """Process the next event from the local queue."""

    if event_queue.empty():
        return None

    event = dequeue_event()
    return process_event(event)


def process_next_sqs_message() -> dict | None:
    """Receive and process one event from AWS SQS."""

    if not AWS_SQS_QUEUE_URL:
        raise ValueError("AWS_SQS_QUEUE_URL is not configured.")

    sqs = boto3.client("sqs", region_name=AWS_REGION)

    response = sqs.receive_message(
        QueueUrl=AWS_SQS_QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10,
    )

    messages = response.get("Messages", [])

    if not messages:
        return None

    message = messages[0]

    # Convert the SQS JSON message into a validated event.
    event = NetworkEvent.model_validate_json(message["Body"])

    # Run the existing incident detection logic.
    result = process_event(event)

    # Generate an alert if an incident was detected.
    alert = create_alert(result["incident"])
    result["alert"] = alert

    # Save the processed event.
    save_record(result)

    # Delete the SQS message only after successful processing.
    sqs.delete_message(
        QueueUrl=AWS_SQS_QUEUE_URL,
        ReceiptHandle=message["ReceiptHandle"],
    )

    return result
