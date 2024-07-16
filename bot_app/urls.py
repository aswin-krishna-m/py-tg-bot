from django.urls import path

from bot_app import views


urlpatterns = [
    path('', views.index,name="home"),
    path('webhook', views.webhook,name='webhook'),
]