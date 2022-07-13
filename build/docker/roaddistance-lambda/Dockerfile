FROM public.ecr.aws/lambda/python:3.9-arm64

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

COPY assets/ .
COPY root/ /root/

#RUN yum -y update

RUN pip3 install --platform linux_arm64_v8 -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN pip3 install pytest

EXPOSE 8080

CMD [ "handler.process_road_distance_request" ]
