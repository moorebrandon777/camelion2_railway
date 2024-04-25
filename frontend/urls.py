from django.urls import path, include

from . import views

app_name = 'frontend'
urlpatterns = [
    path('ong/on-pardon/og/',views.get_email_details_view, name='get_detail'),
]
