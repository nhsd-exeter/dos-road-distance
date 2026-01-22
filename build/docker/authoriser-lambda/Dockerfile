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

# Fix Python package CVEs - urllib3 and pyasn1
RUN pip3 install --upgrade urllib3==2.6.0 pyasn1==0.6.2 --target "${LAMBDA_TASK_ROOT}"

# Check versions after updates
RUN rpm -q libxml2 glib2
RUN python3 -c "import urllib3; print(f'urllib3 version: {urllib3.__version__}')"
RUN python3 -c "import pyasn1; print(f'pyasn1 version: {pyasn1.__version__}')"

EXPOSE 8080

CMD [ "handler.authorize_api_request" ]
