## Working Productively on Windows Using Windows Subsystem for Linux 2 and Docker

A relatively common scenario in enterprise is to provide users with a Windows desktop with a relatively small set of tools, and without administrative access.  Depending on the type of work required, this sort of configuration might be perfectly reasonable, but for others it will be productivity-limiting at best.

Here we discuss the use of Windows Subsytem for Linux 2 (WSL2), along with Docker, as a means of end-user enablement that might offer a reasonable compromise between safety and productivity.  WSL2 allows Windows users to install a largely feature-complete version of Linux within Windows itself, which can be used 'remotely' via Visual Studio Code (vscode) for almost anything.  Normal users will have administrative rights within the Linux installation, but will not have any heightened access over the host OS itself, meaning users are free to experiment with little risk to the host.

Linux on WSL is a perfectly reasonable sandpit in its own right&ndash;we can experiment as suggested, and if somehow break the install we can simply blow it away and start again.  Even so, here we use the Linux instance purely to build Docker images and run Docker containers, ensuring the Linux system remains free of clutter, while providing yet another layer of abstraction.  That is, we run tools via Docker, which runs via Linux on WSL2, rather than installing those tools in Windows.  The target tools are then accessed remotely via SSH or similar, or via some other client interface, such as a web browser or web service.

![](slides/media/dev.png)

![](slides/media/client.png)

## Prerequisites

The goal is to demonstrate that we can make Windows a productive environment in an enterprise setting, with only a minimal set of tools to bootrap our efforts.  Specifically, all that is strictly required is:

* WSL2 is enabled on Windows
* Ubuntu 20.04 is installed for WSL2
* Docker is installed on Ubuntu 20.04
* OpenSSH client is enabled
* Visual Studio Code is installed on Windows
* remote extensions are installed for vscode

WSL2 is available on Windows 10, any edition, build 2004 and up, as well as for Windows Server 2016 and higher.  For more installation details, see [Docker on Windows with Windows Subsystem for Linux 2](https://cmhh.github.io/post/docker_wsl2/).  In an enterprise setting, it would be possible to do most of this in a single powershell script, run as administrator on startup, for example.

## Docker Basics

To create a Docker image, we just need a file called `Dockerfile` containing a complete set of instructions for the build.  That is, a container is (or can be) completely reproducible given only the `Dockerfile`, and so it is often sufficient to manage just this in a version controls system.

We'll see `Dockerfile` examples in the following sections, but given a file, all we need to do to actually create a runnable image called `foo` is to run:

```bash
docker build -t foo <path to Dockerfile>
```

Once created, we can then run instances of the image by running something like the following:

```bash
docker run -d --rm --name mycontainer foo 
``` 

## Containers as Generic Development Environments 

Docker containers can be used as isolated development environments.  In an enterprise setting, and with Windows desktops, it is common to block executable files that have not been certified in some way.  However, we can write code, compile it, and run the resulting binaries inside containers, rather than on the host operating system.  Security aside, the approach also proves useful for other reasons.  Namely, it can just be easier to manage a myriad of different build environment, all on a single host.  We can develop standard images for various different use cases&ndash;a container for Java development, or maybe even different containers for different versions of Java or even different build tools (Maven or Gradle, for example), a container for Node.js development, and so on.

Consider the following Dockerfile

```dockerfile
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
```

Those accustomed to working on Linux will find the content of the file relatively straightforward, but in summary the file does the following:

* installs the usual GNU compiler suite
* installs OpenJDK 8 for Java development
* installs git so we can work with git repositories
* installs sbt, a Java and Scala build tool
* installs .NET 5.0 for C# 9 and F# 5 development, including ASP.NET web applications
* installs Node.js for JavaScript development
* installs OpenSSH server so the container can be accessed remotely

To build the container from the [development](docker/development) directory:

```bash
docker build -t development .
```

and to run an instance:

```bash
docker run -d --rm --name development \
  -v $PWD/.ivy2:/root/.ivy2 \
  -v $PWD/.cache:/root/.cache \
  -v $PWD/.npm:/root/.npm \
  -v $PWD/.vscode-server:/root/.vscode-server \
  -e "PUB_KEY=$(cat $HOME/.ssh/id_rsa.pub)" \
  -e "PRIVATE_KEY=$(cat $HOME/.ssh/id_rsa)" \
  -p 23:22 -p 9001:9001 -p 5001:5001 -p 3001:3001 \
  development
```

In this case, we copy our keys to the container _at runtime_ so that we can connect without a password via a standard SSH client.  In particular, we add the following to our SSH config:

```
Host devdocker
  HostName localhost
  Port 23
  User root
```

and we can then use Visual Studio Code to develop in the usual way, but using the running container:

![](img/vscode01.png)

![](img/vscode02.png)

![](img/vscode03.png)

And provided the right ports are open, we can test web services and so forth locally also:

![](img/vscode04.png)

## Deployment via Containers

Applications are routinely deployed using containers.  In this case, we run a simple [seasonal adjustment service](https://github.com/cmhh/seasadj).  The `Dockerfile` is as follows:

```Dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
ENV SHELL /bin/bash

RUN  apt-get update && apt-get -y dist-upgrade && \
  apt-get install -y --no-install-recommends ca-certificates openjdk-8-jre-headless wget gfortran make && \
  mkdir -p /tmp/x13 && \
  cd /tmp/x13 && \
  # wget https://www.census.gov/ts/x13as/unix/x13ashtmlall_V1.1_B39.tar.gz && \
  # tar -xvf x13ashtmlall_V1.1_B39.tar.gz && \
  # mv x13ashtml /usr/bin/ && \
  wget https://www.census.gov/ts/x13as/unix/x13ashtmlsrc_V1.1_B39.tar.gz && \
  tar -xvf x13ashtmlsrc_V1.1_B39.tar.gz && \
  make -j20 -f makefile.gf && \
  mv x13asHTMLv11b39 /usr/bin/x13ashtml && \
  cd / && \
  rm -fR /tmp/x13 && \
  wget https://github.com/cmhh/seasadj/releases/download/0.1.0-SNAPSHOT/seasadj.jar && \
  apt-get remove -y wget gfortran make && \ 
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* 

EXPOSE 9001

ENTRYPOINT ["java", "-cp", "/seasadj.jar", "org.cmhh.seasadj.Service"]
```

In this example, we simply create a basic instance with a Java runtime, and download an [artefact](https://github.com/cmhh/seasadj/releases/download/0.1.0-SNAPSHOT/seasadj.jar) from GitHub to serve as our entrypoint.  Note that the service itself also requires [X13-ARIMA-SEATS](https://www.census.gov/srd/www/x13as/) be present. (Note that an earlier version of the container simply downloaded a precompiled binary, but that this binary seemed to cause a segmentation fault when run.  So, in this version the source is instead downloaded and compiled to produce a working binary.)

As usual, the container is built as follows:

```bash
docker built -t seasadj .
```

and run as follows:

```bash
docker run -d --rm --name seasadj -p 9001:9001 seasadj
```

The service is stateless.  It accepts one or more input specifications as a JSON array, and returns seasonally adjusted data in the same format.  A basic SPA is provided for quick testing, which can be run directly from the file system:

![](img/seasadjclient.png)

Under basic load testing, the service could handle around 230 transactions per second on a laptop with an 8 core AMD Ryzen 5 2500U with Radeon Vega Mobile Gfx 2.00 GHz processor.  And while no security is provided directly, authentication methods can be added easily if required, and communication can be encrypted easily enough using Nginx or similar.

## Databases via Containers

## Analytics via Containers

## Using a Registry