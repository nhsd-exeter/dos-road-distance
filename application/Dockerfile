FROM public.ecr.aws/lambda/python:3.8

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

RUN apk add --no-cache less vim

COPY requirements.txt ./
# COPY handler.py .
# COPY common.py .
# COPY config.py .
# COPY main.py .
# COPY rdlogger.py .
# COPY traveltime_request.py .
COPY . .

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

EXPOSE 8080

CMD [ "handler.process_road_distance_request" ]
