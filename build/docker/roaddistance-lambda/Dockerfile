FROM public.ecr.aws/lambda/python:3.9

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

COPY assets/ .
COPY root/ /root/

RUN /var/lang/bin/pip install --upgrade pip
RUN /var/lang/bin/pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN /var/lang/bin/pip install pytest

EXPOSE 8080

CMD [ "handler.process_road_distance_request" ]
