FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Dependencies useful for local lambda development and debugging
ENV DEPENDENCIES="tar gzip less"

COPY assets/ .

RUN dnf -y update --refresh
RUN dnf -y install $DEPENDENCIES

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Added to fix CVE-2025-7425 vulnerability - use AWS remediation step
RUN dnf clean all && \
    dnf --refresh makecache && \
    dnf check-update && \
    dnf -y update && \
    dnf clean all

# Check libxml2 version after update
RUN rpm -q libxml2

EXPOSE 8080

CMD [ "handler.authorize_api_request" ]
