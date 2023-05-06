from django.conf.urls import url 
from . import views

urlpatterns = [
    #post views
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<year>\d{4})/')
]
