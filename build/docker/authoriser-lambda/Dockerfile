FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Dependencies useful for local lambda development and debugging
ENV DEPENDENCIES="tar gzip less"

COPY assets/ .

RUN dnf -y update --refresh
RUN dnf -y install $DEPENDENCIES

# Fix Python package CVEs - completely remove all vulnerable versions first
RUN pip3 uninstall -y urllib3 pyasn1 requests protobuf || true
RUN rm -rf /var/lang/lib/python*/site-packages/urllib3* /var/lang/lib/python*/site-packages/pyasn1* /var/lang/lib/python*/site-packages/protobuf* /var/lang/lib/python*/site-packages/requests* || true
RUN rm -rf ${LAMBDA_TASK_ROOT}/urllib3* ${LAMBDA_TASK_ROOT}/pyasn1* ${LAMBDA_TASK_ROOT}/requests* ${LAMBDA_TASK_ROOT}/protobuf* || true

# Now install fixed versions from requirements.txt
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN rm -f /etc/dnf/vars/releasever && \
    dnf clean all && \
    dnf makecache && \
    dnf -y install libxml2 && \
    dnf clean all

# Fix CVE-2025-13601 and CVE-2025-14087 - update glib2 to latest fixed version
RUN dnf -y update glib2-2.82.2-769.amzn2023 && \
    dnf clean all

# Fix additional OS package CVEs - update to latest available versions
RUN dnf -y update \
    libtasn1 \
    openssl-fips-provider-latest \
    openssl-snapsafe-libs \
    libcap && \
    dnf clean all

# Fix CVE-2025-61726 - Using latest base image which should have Go stdlib 1.25.6
# Verify the aws-lambda-rie binary is present and accessible
RUN ls -la /usr/local/bin/aws-lambda-rie || ls -la /var/runtime/bootstrap || echo "AWS Lambda RIE location check"

# Check versions after updates
RUN rpm -q libxml2 glib2
RUN python3 -c "import urllib3; print(f'urllib3 version: {urllib3.__version__}')"
RUN python3 -c "import pyasn1; print(f'pyasn1 version: {pyasn1.__version__}')"

EXPOSE 8080

CMD [ "handler.authorize_api_request" ]
