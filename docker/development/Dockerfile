FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN  apt-get update && apt-get -y dist-upgrade && \
  apt-get install -y --no-install-recommends \
    openssh-server openjdk-8-jdk locales apt-transport-https gnupg2 git vim wget curl xz-utils ca-certificates \
    build-essential gfortran && \
  sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=en_US.UTF-8 && \
  echo "deb https://dl.bintray.com/sbt/debian /" | tee -a /etc/apt/sources.list.d/sbt.list && \
  curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | apt-key add && \
  apt-get update && apt-get install -y sbt && \
  curl https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb --output packages-microsoft-prod.deb && \
  dpkg -i packages-microsoft-prod.deb && \
  curl https://nodejs.org/dist/v14.15.1/node-v14.15.1-linux-x64.tar.xz --output node-v14.15.1-linux-x64.tar.xz && \
  tar -xf node-v14.15.1-linux-x64.tar.xz && \
  mv node-v14.15.1-linux-x64 /usr/local/node && \
  echo "export PATH=$PATH:/usr/local/node/bin" >> /etc/bash.bashrc && \
  rm node-v14.15.1-linux-x64.tar.xz && \
  apt-get update && apt-get install -y dotnet-sdk-5.0 && \
  rm packages-microsoft-prod.deb && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* 

  EXPOSE 22
  
  CMD mkdir -p /root/.ssh && \
    echo "$PUB_KEY" >> /root/.ssh/authorized_keys && \
    echo "$PUB_KEY" >> /root/.ssh/id_rsa.pub && \
    echo "$PRIVATE_KEY" >> /root/.ssh/id_rsa && \
    chmod 700 /root/.ssh && chmod 600 /root/.ssh/* && \
    service ssh start && \
    tail -f /dev/null
  