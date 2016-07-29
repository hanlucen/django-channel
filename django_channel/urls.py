from django.conf.urls import url

from .views import channel_send, channel_pull


urlpatterns = [
    url(r'^channel_pull/(?P<name>\w{1,32})/$', channel_pull),
    url(r'^channel_send/(?P<name>\w{1,32})/$', channel_send),
]
