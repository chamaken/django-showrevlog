from django.conf.urls import url
from .views import *


app_name = 'showrevlog'

urlpatterns = [
    url(r'^$', index, {'template_name': 'showrevlog/files.html'}, name='index'),
    url(r'^(?P<logfile_id>\d+)/$', show, {'template_name': 'showrevlog/show.html'}, name='show'),
    url(r'^(?P<logfile_id>\d+)/csv$', as_csv, name='csv'),
]
