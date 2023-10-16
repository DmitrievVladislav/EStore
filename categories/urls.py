from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.CategoriesView.as_view()),
    path('categories/<int:category_id>/category_details/', views.SingleCategoryDetails.as_view()),
    path('categories/<int:category_id>/products/', views.ProductsCategoryView.as_view()),
    ]