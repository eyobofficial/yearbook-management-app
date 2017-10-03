from django.conf.urls import url 
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Index URL
    url(r'^$', views.index, name='index'),
    url(r'^yearbook/$', views.yearbook, name='yearbook'),
    url(r'^yearbook/create$', views.yearbook_create, name='yearbook-create'),
    url(r'^yearbook/update$', views.yearbook_update, name='yearbook-update'),
    url(r'^yearbook/submit$', views.yearbook_submit, name='yearbook-submit'),
]