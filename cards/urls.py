from django.conf.urls import url

from .views import SingleCardView, CardListView

urlpatterns = [
    url(r'^add/$', SingleCardView.as_view(), name='detail'),
    url(r'^$', CardListView.as_view(), name='index'),
]