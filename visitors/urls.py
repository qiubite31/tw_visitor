from django.conf.urls import url

from . import views

app_name = 'visitors'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^highchart/(?P<purpose>\w+( \w+)?)/(?P<area>\w+(.\w+)?)/$', views.get_visitor_data, name='get_visitor_data'),
    url(r'^api/(?P<purpose>\w+)/(?P<area>\w+(.\w+)?)/$',
        views.get_detail_visitor_data,
        name='get_detail_visitor_data'),
    # url(r'^highchart/api/get_country/continent/(?P<continent>\w+)/$', views.get_country, name="get_country")
    # url(r'^(?P<area>\w+(.\w+)?)/$', views.show_area_data, name='show_area_data'),
]
