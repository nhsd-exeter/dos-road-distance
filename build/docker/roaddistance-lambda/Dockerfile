FROM public.ecr.aws/amazonlinux/amazonlinux:2023

# Install Lambda Runtime Interface Client
RUN dnf install -y python3.13 python3.13-pip && \
    pip3.13 install awslambdaric && \
    dnf clean all

# Set up Lambda environment
ENV LAMBDA_TASK_ROOT=/var/task
ENV LAMBDA_RUNTIME_DIR=/var/runtime

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Dependencies useful for local lambda development and debugging
ENV DEPENDENCIES="tar gzip less"

COPY assets/ .
COPY root/ /root/

RUN dnf -y update --refresh
RUN dnf -y install $DEPENDENCIES

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN pip3 install pytest

# Added to fix CVE-2025-7425 vulnerability - aggressive update approach
RUN dnf clean all && \
    dnf --refresh makecache && \
    dnf config-manager --set-enabled amzn2023-core && \
    dnf --refresh --best --allowerasing reinstall libxml2 && \
    (dnf update --releasever=2023.8.20250908 libxml2 || \
     dnf downgrade libxml2 && dnf update libxml2 || \
     dnf remove libxml2 && dnf install libxml2) && \
    dnf clean all

# Check libxml2 version after update
RUN rpm -q libxml2

EXPOSE 8080

CMD [ "handler.process_road_distance_request" ]
