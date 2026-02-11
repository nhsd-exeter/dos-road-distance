FROM public.ecr.aws/lambda/python:latest

# Set working directory and environment variables
WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
    DEPENDENCIES="tar gzip less wget"

# Copy application files
COPY assets/ .

# Combine system updates, package installations, CVE fixes, and cleanup in single layer
RUN set -eux && \
    # Update system and install base dependencies
    dnf -y update --refresh && \
    dnf -y install $DEPENDENCIES && \
    \
    # Fix Python package CVEs - remove vulnerable versions
    pip3 uninstall -y urllib3 pyasn1 requests protobuf || true && \
    rm -rf /var/lang/lib/python*/site-packages/{urllib3*,pyasn1*,protobuf*,requests*} \
           ${LAMBDA_TASK_ROOT}/{urllib3*,pyasn1*,requests*,protobuf*} || true && \
    \
    # Install fixed Python packages
    pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" && \
    \
    # Fix CVE-2025-7425, CVE-2025-13601, CVE-2025-14087 and install secure package versions
    rm -f /etc/dnf/vars/releasever && \
    dnf clean all && \
    dnf makecache --refresh && \
    dnf -y install libxml2 && \
    dnf -y update glib2 && \
    dnf -y install \
        'libtasn1-4.19.0-1.amzn2023.0.6.x86_64' \
        'libcap-2.73-1.amzn2023.0.6.x86_64' \
        'openssl-fips-provider-latest-3.2.2-1.amzn2023.0.4.x86_64' \
        'openssl-snapsafe-libs-3.2.2-1.amzn2023.0.4.x86_64' || \
    dnf -y update libtasn1 libcap openssl-fips-provider-latest openssl-snapsafe-libs && \
    \
    # Fix go/stdlib CVE by updating aws-lambda-rie to version with Go 1.26.0-rc.3
    wget -O /tmp/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/download/v1.22/aws-lambda-rie-x86_64 && \
    chmod +x /tmp/aws-lambda-rie && \
    mv /tmp/aws-lambda-rie /usr/local/bin/aws-lambda-rie && \
    \
    # Verify installations and versions
    echo "Package versions after update:" && \
    rpm -q libtasn1 libcap openssl-fips-provider-latest openssl-snapsafe-libs libxml2 glib2 && \
    ls -la /usr/local/bin/aws-lambda-rie && \
    python3 -c "import urllib3; print(f'urllib3 version: {urllib3.__version__}')" && \
    python3 -c "import pyasn1; print(f'pyasn1 version: {pyasn1.__version__}')" && \
    \
    # Clean up to reduce layer size
    dnf -y remove wget && \
    dnf clean all && \
    rm -rf /var/cache/dnf/* /tmp/* /var/tmp/*

EXPOSE 8080
CMD [ "handler.authorize_api_request" ]

# Check versions after updates
RUN rpm -q libxml2 glib2
RUN python3 -c "import urllib3; print(f'urllib3 version: {urllib3.__version__}')"
RUN python3 -c "import pyasn1; print(f'pyasn1 version: {pyasn1.__version__}')"

EXPOSE 8080

CMD [ "handler.authorize_api_request" ]
