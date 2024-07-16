from django.urls import path

from bot_app import views


urlpatterns = [
    path('', views.index,name="home"),
    path('setwebhook', views.setwebhook,name='setwebhook'),
    path('webhook', views.webhook,name='webhook'),
]