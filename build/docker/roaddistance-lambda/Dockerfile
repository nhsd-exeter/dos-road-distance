FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Dependencies useful for local lambda development and debugging
ENV DEPENDENCIES="tar gzip less"

COPY assets/ .
COPY root/ /root/

# Single dnf operation: upgrade all (ensures patched libxml2) then install extras; fix CVE (libxml2)
RUN set -eux; \
    dnf -y upgrade --refresh; \
    dnf -y install $DEPENDENCIES; \
    rpm -q libxml2; \
    dnf clean all; \
    rm -rf /var/cache/dnf

RUN pip3 install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}" && \
    pip3 install --no-cache-dir pytest && \
    rm -rf ~/.cache/pip

# Final libxml2 version check (optional; can be removed later to reduce layer size)
RUN rpm -q --queryformat '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}\n' libxml2

EXPOSE 8080

CMD [ "handler.process_road_distance_request" ]
