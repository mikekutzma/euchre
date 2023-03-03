#/bin/sh

echo requirepass `cat /run/secrets/redispasswd` >> /redis.conf

redis-server /redis.conf 
