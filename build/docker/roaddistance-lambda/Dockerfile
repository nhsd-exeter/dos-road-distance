FROM public.ecr.aws/lambda/python:3.13

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Dependencies useful for local lambda development and debugging
ENV DEPENDENCIES="tar gzip less"

COPY assets/ .
COPY root/ /root/

RUN dnf -y update \
    && dnf -y install $DEPENDENCIES libxml2 libcap libarchive sqlite-libs \
    && dnf clean all

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN pip3 install pytest

EXPOSE 8080

CMD [ "handler.process_road_distance_request" ]
