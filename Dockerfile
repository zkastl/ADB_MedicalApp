FROM postgres:9.3

WORKDIR /root

RUN apt-get update
RUN apt-get install -y wget build-essential unzip libprotobuf-c0-dev protobuf-c-compiler nano
RUN apt-get install -y postgresql-server-dev-9.3

RUN wget https://github.com/citusdata/cstore_fdw/archive/master.zip

RUN unzip master.zip
WORKDIR /root/cstore_fdw-master

RUN PATH=/usr/local/pgsql/bin/:$PATH make
RUN PATH=/usr/local/pgsql/bin/:$PATH make install

WORKDIR /
