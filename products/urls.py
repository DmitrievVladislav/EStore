from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductsView.as_view()),
    path('products/<int:id>/', views.ProductUtils.as_view()),
    ]