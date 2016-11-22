# -*- encoding: utf-8 -*-
import json
import datetime
import redis
import calendar
from django.utils import timezone
from django.utils.timezone import utc
from django.db import connections
from django.db import transaction
from django.conf import settings

from .models import ChannelMessage


CHANNEL_REDIS = redis.StrictRedis(
    **getattr(settings, "CHANNEL_REDIS", {})
)


def send_message(name, data):
    ttl = data["ttl"]
    content = data["content"]
    created_time = timezone.now()
    destroy_time = created_time + datetime.timedelta(seconds=ttl)
    with transaction.atomic(savepoint=False):
        message = ChannelMessage(**{
            "name": name,
            "content": content,
            "created_time": created_time,
            "destroy_time": destroy_time,
        })
        message.save()
    CHANNEL_REDIS.publish(name, json.dumps({
        "content": message.content,
        "timestamp": calendar.timegm(
            message.created_time.utctimetuple()
        ) + message.created_time.microsecond / 1000000.0,
    }))



def get_messages(name, timestamp, limit, order, timeout):
    def _get_messages():

        messages =  ChannelMessage.objects.filter(
            name=name,
            destroy_time__gt=timezone.now(),
            created_time__gt=datetime.datetime.utcfromtimestamp(
                timestamp
            ).replace(
                tzinfo=utc,
                microsecond = int(timestamp * 1000000) % int(timestamp)
            ),
        ).order_by("%created_time" % order)[:limit]
        return [{
            "content": message.content,
            "timestamp": calendar.timegm(
                message.created_time.utctimetuple()
            ) + message.created_time.microsecond / 1000000.0,
        } for message in messages]
    messages = _get_messages()
    connections.close_all()  # clean connections
    if not messages:
        sub = CHANNEL_REDIS.pubsub()
        try:
            sub.subscribe([name, ])
            sub.get_message(True, timeout=timeout)
            while True:
                data = sub.get_message(timeout=timeout)
                if not data:
                    break
                if data and data["type"] == 'message':
                    messages.append(json.loads(data["data"].decode("utf-8")))
                    break
        finally:
            sub.close()
    return messages


def clean_message():
    ChannelMessage.objects.filter(
        destroy_time__lte=timezone.now()        
    ).delete()
