from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cards/$', views.CardList.as_view()),
    url(r'^cards/(?P<pk>[0-9]+)/$', views.CardDetail.as_view()),
]