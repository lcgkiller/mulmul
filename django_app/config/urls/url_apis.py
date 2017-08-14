from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^member/', include('member.urls.urls_api')),
    url(r'^post/', include('post.urls.urls_apis')),
]