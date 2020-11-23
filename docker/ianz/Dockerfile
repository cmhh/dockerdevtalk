FROM ubuntu:20.04

ARG ianz_version=1.0-SNAPSHOT
ENV DEBIAN_FRONTEND noninteractive
ENV SHELL /bin/bash

RUN  apt-get update && apt-get -y dist-upgrade && \
  apt-get install -y --no-install-recommends ca-certificates openjdk-8-jre-headless wget unzip locales && \
  sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=en_US.UTF-8 && \
  wget https://github.com/cmhh/ianzpoc/releases/download/${ianz_version}/ianzpoc-${ianz_version}.zip && \
  unzip ianzpoc-${ianz_version}.zip && \
  mv ianzpoc-${ianz_version} ianz && \
  rm ianzpoc-${ianz_version}.zip && \
  apt-get remove -y wget unzip && \ 
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* 

ENV LC_ALL en_US.UTF-8

EXPOSE 9000

WORKDIR /ianz

ENTRYPOINT ["bin/ianzpoc"]
