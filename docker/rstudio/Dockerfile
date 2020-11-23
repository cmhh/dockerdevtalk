ARG ubuntu_version=20.04

FROM ubuntu:$ubuntu_version

ARG cores=12
ARG r_version=4.0.3
ARG rstudio_version=1.4.1032
ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash

RUN  apt-get update && apt-get -y dist-upgrade && \
  apt-get install -y --no-install-recommends \
    gnupg2 dirmngr ca-certificates build-essential \
    libcairo2-dev '^perl-modules-[0-9].[0-9]+$' \
    libssl-dev libgit2-dev libcurl4-gnutls-dev libxml2-dev curl wget htop locales \
    openjdk-8-jdk python3-pip git vim libudunits2-dev \
    grass gdal-bin libgdal-dev libgeos-dev libproj-dev proj-bin proj-data \
    libblas3 libatlas-base-dev liblapack-dev libreadline-dev gfortran \
    libx11-dev libxt-dev zlib1g-dev libbz2-dev liblzma-dev libpcre2-dev \
    sudo lsb-release gdebi-core psmisc libclang-dev libapparmor1 && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=en_US.UTF-8 && \
  wget -qO- "https://yihui.org/gh/tinytex/tools/install-unx.sh" | sh -s - --admin --no-path && \
  mv /root/.TinyTeX /usr/local/TinyTex && \
  /usr/local/TinyTex/bin/*/tlmgr path add && \
  mkdir /src && \
  cd /src && \
  wget https://cran.r-project.org/src/base/R-$(echo $r_version | cut -d'.' -f 1)/R-${r_version}.tar.gz && \
  tar -xvf R-${r_version}.tar.gz && \
  cd /src/R-${r_version} && \
  ./configure --enable-R-shlib --with-blas --with-lapack --enable-memory-profiling --with-cairo && \
  make -j $cores && make install && \
  ln -s /usr/local/lib/R/bin/R /usr/bin/R && \
  ln -s /usr/local/lib/R/bin/Rscript /usr/bin/Rscript && \
  cd / && rm -fR src && \
  echo "local({\n  r <- getOption('repos')\n  r['CRAN'] <- 'https://cloud.r-project.org'\n  options(repos = r)\n})" > /usr/local/lib/R/etc/Rprofile.site && \
  echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" > /usr/local/lib/R/etc/Renviron.site && \
  R -e "install.packages('renv')" && \
  wget https://s3.amazonaws.com/rstudio-ide-build/server/bionic/amd64/rstudio-server-${rstudio_version}-amd64.deb && \
  gdebi --non-interactive rstudio-server-${rstudio_version}-amd64.deb && \
  rm rstudio-server-${rstudio_version}-amd64.deb
  
RUN adduser --disabled-password --gecos "" guest && \
  usermod --password $(openssl passwd -1 guest) guest && \
  usermod -aG sudo guest 

EXPOSE 8787

CMD service rstudio-server start && \
  tail -f /dev/null