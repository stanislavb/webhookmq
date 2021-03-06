#!/usr/bin/env python3
import argparse
from kombu import Connection


def get_message(mq_uri, queue):
    with Connection(mq_uri) as conn:
        simple_queue = conn.SimpleQueue(queue)
        try:
            message = simple_queue.get(block=True, timeout=1)
            message.ack()
            payload = message.payload
        except simple_queue.Empty:
            payload = None
        simple_queue.close()
        return payload

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mq', required=True, help='MQ URI')
    parser.add_argument('--queue', '-q', required=True, help='Queue name')
    args = parser.parse_args()

    message = get_message(args.mq, args.queue)
    if message:
        print("Received: %s" % message)
    else:
        print("Queue empty")
