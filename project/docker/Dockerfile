FROM python:3.7
MAINTAINER Andrew Smirnov <smirnov@informatics.ru>
ADD ./ /network_confrontation
WORKDIR /network_confrontation/
CMD exec apt-get update
CMD exec apt-get install python3-dev libmysqlclient-dev build-essential nano
RUN pip install --no-cache-dir -r ./project/requirements.txt
CMD exec ./project/docker/run.sh
