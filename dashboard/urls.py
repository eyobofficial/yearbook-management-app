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
    url(r'^events/$', views.EventList.as_view(), name='event-list'),
    url(r'^event/(?P<pk>[0-9]+)$', views.EventDetail.as_view(), name='event-detail'),
    url(r'^subscribe/$', views.subscribe_to_event, name='event-subscribe'),
    url(r'^payments/$', views.PaymentList.as_view(), name='payment-list'),
    url(r'payment/(?P<pk>[0-9]+)$', views.PaymentDetail.as_view(), name='payment-detail'),
    url(r'^account/$', views.AccountDetail.as_view(), name='account-detail'),
    url(r'^account/update/$', views.account_update, name='account-update'),
    url(r'^account/change_photo/$', views.change_profile_photo, name='change-photo'),
]