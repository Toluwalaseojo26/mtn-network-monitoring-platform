output "network_events_queue_url" {
  description = "URL of the main network events queue"
  value       = aws_sqs_queue.network_events.url
}

output "network_events_queue_arn" {
  description = "ARN of the main network events queue"
  value       = aws_sqs_queue.network_events.arn
}

output "network_events_dlq_url" {
  description = "URL of the dead letter queue"
  value       = aws_sqs_queue.network_events_dlq.url
}
