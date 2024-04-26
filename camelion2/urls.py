from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('frontend/',include('frontend.urls', namespace='frontend') ),
]

urlpatterns += staticfiles_urlpatterns()
