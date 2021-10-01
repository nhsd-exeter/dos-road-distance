output "lambda_arn" {
  description = "ARN value  for the RD Lambda function"
  value       = aws_lambda_function.road_distance_lambda.arn
}

output "lambda_latest_version" {
  description = "Latest deployed version of the Lambda"
  value       = aws_lambda_function.road_distance_lambda.version
}
