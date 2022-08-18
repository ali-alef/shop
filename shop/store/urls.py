from django.urls import path
from . import views
from .views import productListView, productDetailView, productCreateView, productUpdateView

urlpatterns = [
    path('', productListView.as_view(), name='store'),
    path('product/add/', productCreateView.as_view(), name='create-product'),
    path('product/update/<int:pk>/', productUpdateView.as_view(), name='update-product'),
    path('product/<int:pk>/', productDetailView.as_view(), name='product-detail'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update-item'),
    path('process_order/', views.processOrder, name='process-order'),
]
