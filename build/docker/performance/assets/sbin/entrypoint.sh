#!/bin/bash
cd /opt/locust
BUILD_DATE=$(date +"%Y-%m-%dT%H:%M:%S")
if [[ $PROFILE == "local" ]]
then
  echo "Local Performance Tests"
  locust --config locust.conf --host ${API_ENDPOINT}
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
  echo locust --config locust.conf --host ${API_ENDPOINT} >> ${OUTPUT_FILE}
  locust --config locust.conf --host ${API_ENDPOINT} 2>&1 >> ${OUTPUT_FILE}
  echo "Performance tests finished" >> ${OUTPUT_FILE}
  cd results
  zip -r results.zip ./
  aws s3 cp results.zip s3://${SERVICE_PREFIX}-performance/${ENVIRONMENT}-${BUILD_DATE}.zip
fi
