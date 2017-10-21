from django.conf.urls import url
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Index URL
    url(r'^$', views.index, name='index'),

    # Yearbook URLs
    url(r'^yearbook/$', views.yearbook, name='yearbook'),
    url(r'^yearbook/create$', views.yearbook_create, name='yearbook-create'),
    url(r'^yearbook/update$', views.yearbook_update, name='yearbook-update'),
    url(r'^yearbook/submit$', views.yearbook_submit, name='yearbook-submit'),

    # Polls URLs
    url(r'^polls/$', views.PollList.as_view(), name='poll-list'),
    url(r'^poll/(?P<pk>[0-9]+)$', views.PollDetail.as_view(), name='poll-detail'),
    url(r'^poll/(?P<pk>[0-9]+)/vote/$', views.vote, name='poll-vote'),
    url(r'^poll/(?P<pk>[0-9]+)/result/$', views.poll_result, name='poll-result'),
    url(r'^poll/(?P<pk>[0-9]+)/choice/new/$', views.ChoiceCreate.as_view(), name='choice-create'),
    url(r'^poll/choice/(?P<pk>[0-9]+)/update/$', views.ChoiceUpdate.as_view(), name='choice-update'),
    url(r'^poll/choice/(?P<pk>[0-9]+)/delete/$', views.ChoiceDelete.as_view(), name='choice-delete'),
    url(r'^poll/add/$', views.PollCreate.as_view(), name='poll-create'),
    url(r'^poll/update/(?P<pk>[0-9]+)$', views.PollUpdate.as_view(), name='poll-update'),
    url(r'^poll/delete/(?P<pk>[0-9]+)$', views.PollDelete.as_view(), name='poll-delete'),

    # Events URLs
    url(r'^events/$', views.EventList.as_view(), name='event-list'),
    url(r'^event/(?P<pk>[0-9]+)$', views.EventDetail.as_view(), name='event-detail'),
    url(r'^event/add/$', views.EventCreate.as_view(), name='event-create'),
    url(r'^event/update/(?P<pk>[0-9]+)$', views.EventUpdate.as_view(), name='event-update'),
    url(r'^event/delete/(?P<pk>[0-9]+)$', views.EventDelete.as_view(), name='event-delete'),
    url(r'^event/subscribe/$', views.subscribe_to_event, name='event-subscribe'),
    url(r'^event/(?P<pk>[0-9]+)/program/add/$', views.ProgramCreate.as_view(), name='program-create'),
    url(r'^event/(?P<event_pk>[0-9]+)/program/(?P<pk>[0-9]+)/update/$', views.ProgramUpdate.as_view(), name='program-update'),
    url(r'^event/(?P<event_pk>[0-9]+)/program/(?P<pk>[0-9]+)/delete/$', views.ProgramDelete.as_view(), name='program-delete'),

    # Payments URLs
    url(r'^payments/$', views.PaymentList.as_view(), name='payment-list'),
    url(r'^payment/(?P<pk>[0-9]+)$', views.PaymentDetail.as_view(), name='payment-detail'),
    url(r'^payment/add/$', views.PaymentCreate.as_view(), name='payment-create'),
    url(r'^payment/update/(?P<pk>[0-9]+)$', views.PaymentUpdate.as_view(), name='payment-update'),
    url(r'^payment/delete/(?P<pk>[0-9]+)$', views.PaymentDelete.as_view(), name='payment-delete'),
     
    # Account URLs  
    url(r'^account/$', views.AccountDetail.as_view(), name='account-detail'),
    url(r'^account/update/$', views.account_update, name='account-update'),
    url(r'^account/change_photo/$', views.change_profile_photo, name='change-photo'),

    # Students URLs
    url(r'^students/$', views.StudentList.as_view(), name='student-list'),
    url(r'^student/(?P<pk>[0-9]+)$', views.StudentDetail.as_view(), name='student-detail'),
    url(r'^student/(?P<pk>[0-9]+)/activate/$', views.student_activate, name='student-activate'),
    url(r'^student/(?P<pk>[0-9]+)/deactivate/$', views.student_deactivate, name='student-deactivate'),
]