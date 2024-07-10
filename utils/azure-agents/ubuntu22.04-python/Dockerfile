FROM devopsagentubuntu22.04-base:latest

COPY scripts /scripts

RUN find /scripts/ -type f -exec chmod a+x {} \;

ENV AGENT_TOOLSDIRECTORY=/_work/_tool

RUN apt-get update && apt-get install make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libsqlite3-dev \
    unixodbc-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libreadline-dev \
    libffi-dev \
    wget \
    net-tools \
    mc \
    default-jre

RUN /scripts/installers/python_from_source.sh "3.10.11" && \
    /scripts/installers/allure_commandline.sh "2.28.0" && \
    /scripts/installers/google_chrome_latest.sh
