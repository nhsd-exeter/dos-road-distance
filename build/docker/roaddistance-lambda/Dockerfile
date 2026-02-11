FROM public.ecr.aws/lambda/python:latest

# Set working directory and environment variables
WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
    DEPENDENCIES="tar gzip less wget"

# Copy application files
COPY assets/ .
COPY root/ /root/

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
    pip3 install pytest && \
    \
    # Fix multiple CVEs by installing secure package versions
    # CVE-2025-7425: libxml2 vulnerability
    # CVE-2025-13601, CVE-2025-14087: glib2 vulnerabilities
    # CVE-2025-13151: libtasn1 stack buffer overflow (HIGH)
    # CVE-2025-68121, CVE-2025-61726, CVE-2025-61731, CVE-2025-68119: libcap vulnerabilities (CRITICAL/HIGH)
    # CVE-2025-15467: OpenSSL AEAD cipher vulnerabilities (HIGH)
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
    # Fix go/stdlib CVEs by updating aws-lambda-rie to version with Go 1.26.0-rc.3 or later
    # CVE-2025-68121: TLS session resumption vulnerability (CRITICAL)
    # CVE-2025-22871: HTTP request smuggling vulnerability (CRITICAL)
    # CVE-2025-61725: ParseAddress CPU consumption (HIGH)
    # CVE-2025-61726: URL query parameter memory consumption (HIGH)
    # CVE-2025-61729: HostnameError resource consumption (HIGH)
    # CVE-2025-47907: Database query race condition (HIGH)
    # CVE-2025-58187: Certificate name constraint processing (HIGH)
    # CVE-2025-58188: DSA certificate validation panic (HIGH)
    # CVE-2025-61723: PEM parsing performance issue (HIGH)
    wget -O /tmp/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/download/v1.32/aws-lambda-rie-x86_64 && \
    chmod +x /tmp/aws-lambda-rie && \
    mv /tmp/aws-lambda-rie /usr/local/bin/aws-lambda-rie && \
    \
    # Verify installations and versions
    echo "=== Package versions after CVE fixes ===" && \
    rpm -q libtasn1 libcap openssl-fips-provider-latest openssl-snapsafe-libs libxml2 glib2 && \
    ls -la /usr/local/bin/aws-lambda-rie && \
    echo "=== Python package versions ===" && \
    python3 -c "import urllib3; print(f'urllib3 version: {urllib3.__version__}')" && \
    python3 -c "import pyasn1; print(f'pyasn1 version: {pyasn1.__version__}')" && \
    \
    # Clean up to reduce layer size
    dnf -y remove wget && \
    dnf clean all && \
    rm -rf /var/cache/dnf/* /tmp/* /var/tmp/*

EXPOSE 8080
CMD [ "handler.process_road_distance_request" ]
