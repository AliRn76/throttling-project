#! /bin/bash

docker run \
--restart always \
--name mysql \
--env MYSQL_DATABASE=throttling \
--env MYSQL_ROOT_PASSWORD=ali123 \
--env MYSQL_ROOT_HOST=% \
--volume /srv/docker/mysql:/var/lib/mysql \
-p 3306:3306 \
-d \
mysql/mysql-server
