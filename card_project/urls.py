from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cards/', include('cards.urls')),
    url(r'^api-token-auth/', 'jwt_auth.views.obtain_jwt_token'),
]
