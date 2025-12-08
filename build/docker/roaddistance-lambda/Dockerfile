FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

COPY assets/ .
COPY root/ /root/

# Update system packages and install dependencies in single layer
RUN dnf -y update --refresh && \
    dnf -y install tar gzip less libxml2 && \
    dnf clean all

# Install Python dependencies with security updates
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" && \
    pip3 install pytest && \
    pip3 install --upgrade "urllib3==2.6.0" --target "${LAMBDA_TASK_ROOT}"

EXPOSE 8080

CMD [ "handler.process_road_distance_request" ]
