FROM python:3.8

COPY assets/sbin /sbin
RUN chmod -R 777 /sbin

WORKDIR /opt
RUN mkdir -p locust
RUN apt-get update && apt-get install -y zip

WORKDIR /opt/locust
RUN mkdir -p results
COPY assets/locust /opt/locust/
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/sbin/entrypoint.sh" ]
