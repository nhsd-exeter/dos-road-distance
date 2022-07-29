FROM public.ecr.aws/lambda/python:3.9

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

COPY assets/ .

RUN yum -y update

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

EXPOSE 8080

CMD [ "handler.authorize_api_request" ]
