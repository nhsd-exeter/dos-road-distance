output "api_execution_arn" {
  description = "Execution ARN value for the API Gateway"
  value       = aws_apigatewayv2_api.road_distance_apigateway.execution_arn
}

output "api_id" {
  description = "ID of the API Gateway"
  value       = aws_apigatewayv2_api.road_distance_apigateway.id
}
