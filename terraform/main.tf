terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_sqs_queue" "network_events_dlq" {
  name                      = "mtn-network-events-dlq"
  message_retention_seconds = 1209600

  tags = {
    Project     = "MTN Network Monitoring"
    Environment = "Development"
    Purpose     = "Dead letter queue"
  }
}

resource "aws_sqs_queue" "network_events" {
  name                       = "mtn-network-events"
  visibility_timeout_seconds = 60
  message_retention_seconds  = 345600

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.network_events_dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Project     = "MTN Network Monitoring"
    Environment = "Development"
    Purpose     = "Incoming network events"
  }
}
