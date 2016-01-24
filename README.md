# WebhookMQ
![Build status](https://circleci.com/gh/stanislavb/webhookmq.svg?style=shield&circle-token=a6876dda60739f563d1c8e71fa3ffbb4a1aa723a)

Receive webhooks and put them into a message queue.

Built in python using Django for web requests and kombu for message queue handling.

## Message queues supported
The kombu library supports amqp, qpid, redis, mongodb and more: http://kombu.readthedocs.org/en/latest/userguide/connections.html

## Webhooks supported
Note that this app has no security. Any POST request to an endpoint using the right path prefix will result in an attempt to put a message on a queue, as long as request contents can be decoded as JSON or a key-value multipart/form-data.

The way to avoid abuse is to restrict access to this app in a firewall and validate message contents when consuming them from the queue.

    http(s)://hostname.example.com/path/queue_name

On a successful request, HTTP 200 OK is returned. On some errors, content returned will be a JSON structure with a 'message' key.

## Build
Either pull an image automatically built from this repo (https://hub.docker.com/r/stanislavb/webhookmq/):

    docker pull stanislavb/webhookmq

Or build your own:

    make build

## Test
Test code standards (requires flake8 installed):

    make syntax-test

Test integration with RabbitMQ:

    make docker-integration-test

## Deploy
Hosting of a message queue is not covered by this document, but if you have one provisioned, you can scale WebhookMQ horisontally just by starting more with same settings.

    docker run -d \
        -e "SECRET_KEY=foo" \
        -e "PATH_PREFIX=webhook" \
        -e "MQ_URI=amqp://user:password@mq.example.com/vhost/" \
        stanislavb/webhookmq

The command above would start the service and accept POST requests at http://(container ip):8080/webhook/(queue_name)/

### Use nginx proxy
It is extremely recommended to use a robust web server in front of any web application. You could for example use jwilder/nginx-proxy:

    docker run -d \
        --name nginx-proxy \
        -v /var/run/docker.sock:/tmp/docker.sock:ro \
        -p 80:80 \
        jwilder/nginx-proxy

    docker run -d \
        -e "SECRET_KEY=foo" \
        -e "PATH_PREFIX=webhook" \
        -e "MQ_URI=amqp://user:password@mq.example.com/vhost/" \
        -e "VIRTUAL_HOST=public.example.com" \
        stanislavb/webhookmq

Provided DNS record for public.example.com would be pointing at this docker host machine, the service would accept POST requests at http://public.example.com/webhook/(queue_name)/
