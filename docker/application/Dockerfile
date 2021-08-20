FROM public.ecr.aws/lambda/python:3.8

WORKDIR ${LAMBDA_TASK_ROOT}

COPY application/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY ../../application .

#CMD [ "python", "./your-daemon-or-script.py" ]
CMD [ "handler.process_road_distance_request"]
