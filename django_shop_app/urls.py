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
    path('c/<int:category_id>/', views.category_products, name='category_products'),
    path('p/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin_panel/add_category/', views.add_category, name='add_category'),
    path('admin_panel/add_product/', views.add_product, name='add_product'),
    path('admin_panel/product_list/', views.product_list, name='product_list'),
    path('admin_panel/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('admin_panel/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin_panel/order_list/', views.order_list, name='order_list'),
    path('admin_panel/order_details/<int:order_id>/', views.order_details, name='order_details'),
    path('user_panel/', views.user_panel, name='user_panel'),
    path('user_panel/user_orders/', views.user_orders, name='user_orders'),
    path('change_password/', views.change_password, name='change_password'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)