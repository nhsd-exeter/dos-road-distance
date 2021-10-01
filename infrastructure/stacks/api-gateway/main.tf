resource "aws_apigatewayv2_api" "road_distance_apigateway" {
  name          = "${var.service_prefix}-rd-api-gateway"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "road_distance_api_integration" {
  api_id                 = aws_apigatewayv2_api.road_distance_apigateway.id
  payload_format_version = "2.0"
  integration_type       = "AWS_PROXY"
  integration_method     = "POST"
  integration_uri        = "${data.terraform_remote_state.lambda.outputs.lambda_arn}:$${stageVariables.version}"
}

resource "aws_apigatewayv2_stage" "road_distance_api_stage" {
  api_id      = aws_apigatewayv2_api.road_distance_apigateway.id
  name        = "$default"
  auto_deploy = true
  stage_variables = {
    "version" = data.terraform_remote_state.lambda.outputs.lambda_latest_version
  }
}

resource "aws_apigatewayv2_route" "road_distance_api_route" {
  api_id    = aws_apigatewayv2_api.road_distance_apigateway.id
  route_key = "POST /"
  target    = "integrations/${aws_apigatewayv2_integration.road_distance_api_integration.id}"
}

resource "aws_lambda_permission" "road_distance_invoke_lambda_permission" {
  action        = "lambda:InvokeFunction"
  function_name = "${var.service_prefix}-rd-lambda"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.road_distance_apigateway.execution_arn}/*/*/"
}

# Auth probably required also
