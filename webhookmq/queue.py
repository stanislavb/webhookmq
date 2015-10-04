import kombu
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from webhookmq import settings


@require_http_methods(["POST"])
@csrf_exempt
def send_message(request, path_prefix, queue):
    assert path_prefix == settings.PATH_PREFIX
    message = request.POST
    with kombu.Connection(settings.MQ_URI) as connection:
        simple_queue = connection.SimpleQueue(queue)
        simple_queue.put(message, serializer='json', compression='zlib')
        return HttpResponse(status=200)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line()
