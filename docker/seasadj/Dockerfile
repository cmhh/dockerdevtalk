FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
ENV SHELL /bin/bash

RUN  apt-get update && apt-get -y dist-upgrade && \
  apt-get install -y --no-install-recommends ca-certificates openjdk-8-jre-headless wget && \
  mkdir -p /tmp/x13 && \
  cd /tmp/x13 && \
  wget https://www.census.gov/ts/x13as/unix/x13ashtmlall_V1.1_B39.tar.gz && \
  tar -xvf x13ashtmlall_V1.1_B39.tar.gz && \
  mv x13ashtml /usr/bin/ && \
  cd / && \
  rm -fR /tmp/x13 && \
  wget https://github.com/cmhh/seasadj/releases/download/0.1.0-SNAPSHOT/seasadj.jar && \
  apt-get remove -y wget && \ 
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* 

EXPOSE 9001

ENTRYPOINT ["java", "-cp", "/seasadj.jar", "org.cmhh.seasadj.Service"]