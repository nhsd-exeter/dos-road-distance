FROM public.ecr.aws/lambda/python:3.8

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

RUN pip3 install bcrypt
COPY assets/ .

EXPOSE 8080

CMD [ "handler.authorize_api_request" ]
