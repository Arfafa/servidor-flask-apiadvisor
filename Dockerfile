FROM ubuntu:18.04

RUN apt update -y && \
    apt install -y python3-pip python3-dev build-essential

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]

CMD ["entry_point.py"]
