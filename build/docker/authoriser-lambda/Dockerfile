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
RUN rm -f /etc/dnf/vars/releasever && \
    dnf clean all && \
    dnf makecache && \
    dnf -y install libxml2 && \
    dnf clean all

# Fix CVE-2025-13601 and CVE-2025-14087 - update glib2 to latest fixed version
RUN dnf -y update glib2-2.82.2-769.amzn2023 && \
    dnf clean all

# Fix Python package CVEs - completely remove all versions and clean install
RUN pip3 uninstall -y urllib3 pyasn1 requests || true
RUN rm -rf /var/lang/lib/python*/site-packages/urllib3* /var/lang/lib/python*/site-packages/pyasn1* || true
RUN rm -rf ${LAMBDA_TASK_ROOT}/urllib3* ${LAMBDA_TASK_ROOT}/pyasn1* ${LAMBDA_TASK_ROOT}/requests* || true
RUN pip3 install urllib3==2.6.3 pyasn1==0.6.2 requests==2.32.4 certifi charset-normalizer idna --target "${LAMBDA_TASK_ROOT}" --no-cache-dir

# Fix CVE-2025-61726 - Update AWS Lambda RIE to version with Go stdlib 1.25.6
RUN curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie && \
    chmod +x /usr/local/bin/aws-lambda-rie

# Check versions after updates
RUN rpm -q libxml2 glib2
RUN python3 -c "import urllib3; print(f'urllib3 version: {urllib3.__version__}')"
RUN python3 -c "import pyasn1; print(f'pyasn1 version: {pyasn1.__version__}')"

EXPOSE 8080

CMD [ "handler.authorize_api_request" ]
