from django.conf.urls import url 
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Index URL
    url(r'^$', views.index, name='index'),
]