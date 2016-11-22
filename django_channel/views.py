import time
import json
from .helper import get_messages, send_message, clean_message
from django.http import HttpResponse


def channel_pull(request, name):
    limit = int(request.GET.get("limit", 30))
    order = request.GET.get("order", "-")
    timeout = float(request.GET.get("timeouot", 30))
    timestamp = float(request.GET.get("timestamp", time.time()))

    limit = 300 if limit > 300 else limit
    order = "-" if order not in ("+", "-") else order
    messages = get_messages(name, timestamp, limit, order, timeout)
    return HttpResponse(
        content=json.dumps(messages),
        content_type='application/json'
    )


def channel_send(request, name):
    ttl = float(request.POST.get("ttl"))
    content = request.POST.get("content")
    send_message(name, data={"ttl": ttl, "content": content})
    return HttpResponse(status=204, content_type='application/json')


def channel_clean(request):
    clean_message()
    return HttpResponse(status=204, content_type='application/json')
