# WebhookMQ
Receive webhooks and put them into a message queue.

Built in python using Django for web requests and kombu for message queue handling.

## Message queues supported
The kombu library supports amqp, qpid, redis, mongodb and more: http://kombu.readthedocs.org/en/latest/userguide/connections.html

## Webhooks supported
Note that this app has no security. Any POST request to an endpoint using the right path prefix will result in an attempt to put a message on a queue, as long as request contents can be decoded as JSON.

The way to avoid abuse is to restrict access to this app in a firewall and validate message contents when consuming them from the queue.

    http(s)://hostname.example.com/path/queue_name

On a successful request, HTTP 200 OK is returned.
