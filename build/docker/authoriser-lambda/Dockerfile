FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Dependencies useful for local lambda development and debugging
ENV DEPENDENCIES="tar gzip less"

COPY assets/ .

RUN dnf -y update
RUN dnf -y install $DEPENDENCIES

# Added to fix CVE-2025-49796 vulnerability
RUN dnf -y install libxml2-2.10.4-1.amzn2023.0.12 && dnf clean all

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

EXPOSE 8080

CMD [ "handler.authorize_api_request" ]
