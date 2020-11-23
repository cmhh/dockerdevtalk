FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN  apt-get update && apt-get -y dist-upgrade && \
  apt-get install -y --no-install-recommends \
    curl locales git r-base r-base-dev libcurl4-openssl-dev libssl-dev libxml2-dev && \
  sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=en_US.UTF-8 && \
  git clone https://github.com/StatisticsNZ/data_portal.git && \
  R -e "install.packages(c('dplyr', 'configr', 'highcharter', 'shinyjs', \
    'readxl', 'lubridate', 'tidyr', 'stringr', 'jsonlite', 'R6', 'httr', \
    'data.table', 'shiny', 'shinycssloaders', 'foreach'), repos = 'https://cran.rstudio.com')" && \
  apt-get remove -y git r-base-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*  

EXPOSE 3000

CMD R -e "shiny::runApp('/data_portal', host = '0.0.0.0', port = 3000)"

