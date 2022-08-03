#!/bin/bash

mkdir -p /tmp/hw9-otus

docker build --rm -t "hw9-otus:v1" .
docker run --rm --name "hw9-otus" -ti -p 8080:8080 -v /tmp/hw9-otus:/tmp/hw9-otus/ hw9-otus:v1 /bin/bash