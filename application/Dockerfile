FROM public.ecr.aws/lambda/python:3.8

WORKDIR ${LAMBDA_TASK_ROOT}

#COPY requirements.txt ./
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"


#CMD [ "python", "./your-daemon-or-script.py" ]
#CMD [ "application.process_road_distance_request" ]
CMD [ "python", "./main.py"]
