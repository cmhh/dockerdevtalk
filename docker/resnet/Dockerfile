FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
COPY app /app
WORKDIR /app

RUN apt-get update -y && \
  apt-get install -y \
    python3-pip python3-dev libglib2.0-dev libxrender-dev libxext-dev libsm6 && \ 
  pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]