from django.urls import path

from . import views

app_name = "django_shop_app"

urlpatterns = [
    path('', views.index, name='index'),
]
