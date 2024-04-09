from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "django_shop_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('add_category/', views.add_category, name='add_category'),  
    path('add_product/', views.add_product, name='add_product'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)