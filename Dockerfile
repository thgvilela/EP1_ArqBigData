FROM python:3-slim

ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

#ENTRYPOINT ["python3"]
#CMD ["pythongetapi.py"]
