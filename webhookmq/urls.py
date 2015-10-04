from django.conf.urls import url
from webhookmq import queue

urlpatterns = [
    url(r'^(?P<path_prefix>\w+)/(?P<queue>\w+)', queue.send_message)
]
