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
    url(r'^polls/$', views.PollList.as_view(), name='poll-list'),
    url(r'^poll/(?P<pk>[0-9]+)/vote/$', views.poll_detail, name='poll-detail'),
    url(r'^poll/(?P<pk>[0-9]+)/result/$', views.poll_result, name='poll-result'),
]