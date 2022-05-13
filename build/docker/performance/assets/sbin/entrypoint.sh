#!/bin/bash
cd /opt/locust
BUILD_DATE=$(date +"%Y-%m-%dT%H:%M:%S")
if [[ $PROFILE == "local" ]]
then
  echo "Local Performance Tests"
  locust --config locust.conf --host ${API_ENDPOINT}
  echo "Performance tests finished"
  cd /opt/locust/results
  cp report.html /project/test/performance/results/report-${ENVIRONMENT}-${BUILD_DATE}.html
  cp logfile.log /project/test/performance/results/logfile-${ENVIRONMENT}-${BUILD_DATE}.log
  cp csv_stats.csv /project/test/performance/results/csv-stats-${ENVIRONMENT}-${BUILD_DATE}.csv
  cp csv_failures.csv /project/test/performance/results/csv-failures-${ENVIRONMENT}-${BUILD_DATE}.csv
  cp csv_stats_history.csv /project/test/performance/results/csv-stats-history-${ENVIRONMENT}-${BUILD_DATE}.csv
else
  echo "Remote Performance Tests" | tee results/locust.host.log
  echo locust --config locust.conf --host ${API_ENDPOINT}/${ENVIRONMENT}/ | tee -a results/locust.host.log
  locust --config locust.conf --host ${API_ENDPOINT}/${ENVIRONMENT}/ | tee -a results/locust.host.log
  echo "Performance tests finished" | tee -a results/locust.host.log
  cd /opt/locust/results
  zip -r results.zip ./
  aws s3 cp results.zip s3://${SERVICE_PREFIX}-performance/${ENVIRONMENT}-${BUILD_DATE}.zip
fi
