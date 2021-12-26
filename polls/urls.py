from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .views import SearchResultsView


urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.products, name='products'),
    path('<int:id>/detail/', views.detail, name='detail'),
    path('order/', views.checkout, name='order'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('login/', auth_view.LoginView.as_view(template_name='pages/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='pages/logout.html'), name="logout")
]