from django.conf.urls import url

from .views import CardList

urlpatterns = [
    url(r'^cards/$', CardList.as_view(), name='card-list'),
    # url(r'^$', CardListView.as_view(), name='index'),
]