resource "aws_apigatewayv2_api" "road_distance_apigateway" {
  name          = "${var.service_prefix}-rd-api-gateway"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "road_distance_api_integration" {
  api_id             = aws_apigatewayv2_api.road_distance_apigateway.id
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
  integration_uri    = data.terraform_remote_state.lambda.outputs.lambda_arn
}

resource "aws_apigatewayv2_stage" "road_distance_api_stage" {
  api_id = aws_apigatewayv2_api.road_distance_apigateway.id
  name   = var.environment
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.road_distance_lambda_log_group.arn
    format          = "{ \"requestId\":\"$context.requestId\", \"ip\": \"$context.identity.sourceIp\", \"requestTime\":\"$context.requestTime\", \"httpMethod\":\"$context.httpMethod\",\"routeKey\":\"$context.routeKey\", \"status\":\"$context.status\",\"protocol\":\"$context.protocol\", \"responseLength\":\"$context.responseLength\" }"
  }
}

resource "aws_apigatewayv2_route" "road_distance_api_route" {
  api_id    = aws_apigatewayv2_api.road_distance_apigateway.id
  route_key = "POST /"
  target    = "integrations/${aws_apigatewayv2_integration.road_distance_api_integration.id}"
}

# Auth probably required also

resource "aws_cloudwatch_log_group" "road_distance_lambda_log_group" {
  name              = "/aws/api-gateway/${var.service_prefix}-rd-api"
  retention_in_days = "0"
}
