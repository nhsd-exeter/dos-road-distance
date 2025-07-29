#!/bin/bash
cd /opt/locust
BUILD_DATE=$(date +"%Y-%m-%dT%H:%M:%S")

# Validate required environment variables - use PERF_TEST_HOST instead of API_ENDPOINT
if [[ -z "${PERF_TEST_HOST}" ]]; then
  echo "ERROR: PERF_TEST_HOST is not set"
  echo "Current PERF_TEST_HOST: ${PERF_TEST_HOST:-<not set>}"
  echo "Trying LOCUST_HOST as fallback..."
  if [[ -z "${LOCUST_HOST}" ]]; then
    echo "ERROR: LOCUST_HOST is also not set"
    echo "Current LOCUST_HOST: ${LOCUST_HOST:-<not set>}"
    exit 1
  else
    HOST_URL="${LOCUST_HOST}"
  fi
else
  HOST_URL="${PERF_TEST_HOST}"
fi

if [[ -z "${SERVICE_PREFIX}" || "${SERVICE_PREFIX}" == "SERVICE_PREFIX_TO_REPLACE" ]]; then
  echo "ERROR: SERVICE_PREFIX is not set or contains placeholder value"
  echo "Current SERVICE_PREFIX: ${SERVICE_PREFIX:-<not set>}"
  exit 1
fi

if [[ -z "${ENVIRONMENT}" || "${ENVIRONMENT}" == "ENVIRONMENT_TO_REPLACE" ]]; then
  echo "ERROR: ENVIRONMENT is not set or contains placeholder value"
  echo "Current ENVIRONMENT: ${ENVIRONMENT:-<not set>}"
  exit 1
fi

echo "Starting performance tests with:"
echo "  HOST_URL: ${HOST_URL}"
echo "  SERVICE_PREFIX: ${SERVICE_PREFIX}"
echo "  ENVIRONMENT: ${ENVIRONMENT}"
echo "  PROFILE: ${PROFILE}"

if [[ $PROFILE == "local" ]]
then
  echo "Local Performance Tests"
  locust --config locust.conf --host ${HOST_URL}
  echo "Performance tests finished"
  RESULTS_DIR=/project/test/performance/results/
  cp report.html ${RESULTS_DIR}report-${ENVIRONMENT}-${BUILD_DATE}.html
  cp logfile.log ${RESULTS_DIR}logfile-${ENVIRONMENT}-${BUILD_DATE}.log
  cp csv_stats.csv ${RESULTS_DIR}csv-stats-${ENVIRONMENT}-${BUILD_DATE}.csv
  cp csv_failures.csv ${RESULTS_DIR}csv-failures-${ENVIRONMENT}-${BUILD_DATE}.csv
  cp csv_stats_history.csv ${RESULTS_DIR}csv-stats-history-${ENVIRONMENT}-${BUILD_DATE}.csv
else
  OUTPUT_FILE=results/locust.cli.log
  echo "Remote Performance Tests" > ${OUTPUT_FILE}
  echo locust --config locust.conf --host ${HOST_URL} >> ${OUTPUT_FILE}
  locust --config locust.conf --host ${HOST_URL} 2>&1 >> ${OUTPUT_FILE}
  echo "Performance tests finished" >> ${OUTPUT_FILE}
  cd results
  zip -r results.zip ./

  # Check if S3 bucket exists and create if necessary
  S3_BUCKET="${SERVICE_PREFIX}-performance"
  S3_KEY="${ENVIRONMENT}-${BUILD_DATE}.zip"

  echo "Checking if S3 bucket ${S3_BUCKET} exists..."
  if ! aws s3api head-bucket --bucket "${S3_BUCKET}" 2>/dev/null; then
    echo "S3 bucket ${S3_BUCKET} does not exist. Creating it..."
    aws s3 mb "s3://${S3_BUCKET}" || {
      echo "ERROR: Failed to create S3 bucket ${S3_BUCKET}"
      echo "Attempting to upload to alternative location..."
      S3_BUCKET="${SERVICE_PREFIX}-performance-${ENVIRONMENT}"
      echo "Trying bucket: ${S3_BUCKET}"
      if ! aws s3api head-bucket --bucket "${S3_BUCKET}" 2>/dev/null; then
        echo "Creating alternative bucket: ${S3_BUCKET}"
        aws s3 mb "s3://${S3_BUCKET}" || {
          echo "ERROR: Failed to create alternative S3 bucket. Skipping upload."
          exit 0
        }
      fi
    }
  fi

  echo "Uploading results to s3://${S3_BUCKET}/${S3_KEY}"
  aws s3 cp results.zip "s3://${S3_BUCKET}/${S3_KEY}" || {
    echo "ERROR: Failed to upload results to S3"
    exit 1
  }
  echo "Results successfully uploaded to S3"
fi
