from datetime import datetime, timezone
from enum import Enum 

from pydantic import BaseModel, Field

class EventType(str, Enum):
    DROPPED_CALL = "dropped_call"
    HIGH_LATENCY = "high_latency"
    SERVICE_OUTAGE = "service_outage"
    FAILED_TRANSACTION = "failed_transaction"
    DEVICE_FAILURE = "device_failure"
   
class Severity(str, Enum):

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NetworkEvent(BaseModel):
    event_id: str = Field(min_length=1, max_length=100)
    event_type: EventType
    location: str = Field(min_length=1, max_length=100)
    severity: Severity
    description: str = Field(min_length=1, max_length=500)
    timestamp: datetime = Field(
         default_factory=lambda: datetime.now(timezone.utc)
    )  
