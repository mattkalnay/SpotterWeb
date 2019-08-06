from django.conf.urls import url
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    url(r'^messageup/(?P<id>\d+)$', views.upload),
    url(r'^display$', views.display), 
    url(r'^success$', views.success), 
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^registration$', views.registration),
    url(r'^logout$', views.logout),
    url(r'^logprocess$', views.logprocess),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^challenge/(?P<id>\d+)$', views.challenge),
    url(r'^challenge/update/(?P<user_id>\d+)/(?P<id>\d+)$', views.update),
    url(r'^delete/(?P<id>\d+)$', views.remove),
    url(r'^create$', views.create),
    url(r'^createprocess$', views.createprocess),
]
if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT)