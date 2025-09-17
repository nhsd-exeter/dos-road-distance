FROM python:3.12-slim

COPY assets/sbin/ /sbin/
RUN chmod u+x /sbin/*.sh

WORKDIR /opt
RUN mkdir -p locust
RUN apt-get update -y && apt-get install -y zip

WORKDIR /opt/locust
RUN mkdir -p results
COPY assets/locust /opt/locust/
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/sbin/entrypoint.sh" ]
