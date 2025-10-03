FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Dependencies useful for local lambda development and debugging
ENV DEPENDENCIES="tar gzip less"

COPY assets/ .

RUN dnf -y update --refresh
RUN dnf -y install $DEPENDENCIES

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Added to fix CVE-2025-7425 vulnerability - force specific version
RUN rm -f /etc/dnf/vars/releasever
RUN dnf clean all && \
    dnf -y install --releasever 2023.8.20250908 libxml2-2.10.4-1.amzn2023.0.13.x86_64 && \
    dnf clean all

# Check libxml2 version after update
RUN rpm -q libxml2

EXPOSE 8080

CMD [ "handler.authorize_api_request" ]
