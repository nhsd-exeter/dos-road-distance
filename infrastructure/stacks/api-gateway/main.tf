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
  api_id             = aws_apigatewayv2_api.road_distance_apigateway.id
  route_key          = "POST /"
  target             = "integrations/${aws_apigatewayv2_integration.road_distance_api_integration.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.road_distance_api_auth.id
}

resource "aws_lambda_permission" "road_distance_invoke_lambda_permission" {
  action        = "lambda:InvokeFunction"
  function_name = "${var.service_prefix}-rd-lambda"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.road_distance_apigateway.execution_arn}/*/*/"
}

resource "aws_apigatewayv2_authorizer" "road_distance_api_auth" {
  name                              = "${var.service_prefix}-rd-api-authoriser"
  api_id                            = aws_apigatewayv2_api.road_distance_apigateway.id
  authorizer_type                   = "REQUEST"
  authorizer_uri                    = data.terraform_remote_state.lambda.outputs.auth_lambda_arn
  authorizer_payload_format_version = "2.0"
  authorizer_result_ttl_in_seconds  = 0
  enable_simple_responses           = true
  # identity_sources                  = ["event.headers.authorization"]
}

resource "aws_lambda_permission" "auth_invoke_lambda_permission" {
  action        = "lambda:InvokeFunction"
  function_name = "${var.service_prefix}-auth-lambda"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.road_distance_apigateway.execution_arn}/*"
}

resource "aws_cloudwatch_log_group" "road_distance_lambda_log_group" {
  name              = "/aws/api-gateway/${var.service_prefix}-rd-api"
  retention_in_days = "0"
}
