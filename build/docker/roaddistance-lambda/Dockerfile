FROM public.ecr.aws/lambda/python:3.8

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ENV DRD_ENDPOINT="http://localhost"
ENV DRD_BASICAUTH=""
ENV DRD_MOCK_MODE="True"

COPY assets/ .

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN pip3 install pytest

EXPOSE 8080

CMD [ "handler.process_road_distance_request" ]
