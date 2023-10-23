from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductsView.as_view()),
    path('products/<int:product_id>/', views.SingleProductView.as_view()),
    path('products/recommends/', views.RecommendedProductsView.as_view()),
]
