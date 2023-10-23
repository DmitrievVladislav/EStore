from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductsView.as_view()),
    path('products/<int:id>/', views.ProductUtils.as_view()),
    path('products/recommends/', views.RecommendedProductsView.as_view()),
]
