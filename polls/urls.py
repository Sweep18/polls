from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.MainPageView.as_view(), name='main'),
    url(r'^first/$', views.FirstPhaseView.as_view(), name='first'),
    url(r'^second/(?P<pk>[0-9]+)/$', views.SecondPhaseView.as_view(), name='second'),
    url(r'^reset/(?P<pk>[0-9]+)/$', views.ResetPollView.as_view(), name='reset'),
    url(r'^dashboard/$', views.get_data_dashboard, name='dashboard'),
]