resource "aws_apigatewayv2_stage" "road_distance_api_stage" {
  api_id      = data.terraform_remote_state.api_gateway.outputs.api_id
  name        = var.environment
  auto_deploy = true
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.road_distance_lambda_log_group.arn
    format          = "{ \"requestId\":\"$context.requestId\", \"ip\": \"$context.identity.sourceIp\", \"requestTime\":\"$context.requestTime\", \"httpMethod\":\"$context.httpMethod\",\"routeKey\":\"$context.routeKey\", \"status\":\"$context.status\",\"protocol\":\"$context.protocol\", \"responseLength\":\"$context.responseLength\", \"error\":\"$context.error.message\", \"authError\":\"$context.authorizer.error\", \"integrationError\":\"$context.integration.error\" }"
  }
  stage_variables = {
    "version" = var.lambda_version
  }
}

resource "aws_lambda_alias" "latest-rd-lambda-version" {
  name             = "latest-rd-lambda-version"
  function_name    = "${var.service_prefix}-rd-lambda"
  function_version = aws_lambda_function.road_distance_lambda.version
}

resource "aws_lambda_permission" "road_distance_invoke_lambda_permission" {
  action        = "lambda:InvokeFunction"
  function_name = "${var.service_prefix}-rd-lambda:${var.lambda_version}"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${data.terraform_remote_state.api_gateway.outputs.api_execution_arn}/*/*/"
  depends_on    = [aws_lambda_alias.latest-rd-lambda-version]
}

resource "aws_cloudwatch_log_group" "road_distance_lambda_log_group" {
  name              = "/aws/api-gateway/${var.service_prefix}-rd-api/${var.environment}"
  retention_in_days = "0"
}
