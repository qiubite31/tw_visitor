from django.conf.urls import url

from . import views

app_name = 'visitors'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<visitor_id>[0-9]+)/$', views.get_visitor, name='visitor'),
    url(r'^(?P<month>[0-9]{4}-[0-9]{2})/$', views.visitor_reason, name='reason'),
    url(r'^(?P<month>[0-9]{4}-[0-9]{2})/(?P<reason>\w+ \w+( \w+)?)/$', views.visitor_detail, name='detail')
]
