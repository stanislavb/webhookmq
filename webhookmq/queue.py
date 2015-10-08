import kombu
import logging
import socket
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseNotFound
from webhookmq import settings

logger = logging.getLogger()


def queue_message(message, queue):
    logger.info('Message to put on MQ "{}" queue "{}": {}'.format(
        settings.MQ_URI, queue, message))
    try:
        with kombu.Connection(settings.MQ_URI) as connection:
            simple_queue = connection.SimpleQueue(queue)
            simple_queue.put(message, serializer='json', compression='zlib')
        return True
    except socket.gaierror:
        logger.exception('Could not reach MQ "{}". Please check your MQ_URI environment variable'.format(
            settings.MQ_URI))
        return False


@require_http_methods(["POST"])
@csrf_exempt
def receive_message(request, path_prefix, queue):
    if path_prefix != settings.PATH_PREFIX:
        return HttpResponseNotFound()
    try:
        decoded_message = request.body.decode('utf-8')
        message = json.loads(decoded_message)
    except json.decoder.JSONDecodeError:
        # We have invalid JSON. Let's try Django's QueryDict.
        message = request.POST
    logger.info('Received message: {}'.format(message))
    if len(message) == 0:
        return JsonResponse({"message": "Empty POST request"}, status=400)
    queued = queue_message(message, queue)
    if queued:
        return JsonResponse(message, status=200)
    else:
        return JsonResponse({"message": "No connection to message queue"}, status=500)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line()
