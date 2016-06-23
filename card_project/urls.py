from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from cards import views

router = DefaultRouter()
router.register(r'cards', views.CardViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('cards.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
