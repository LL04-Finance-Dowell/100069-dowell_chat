from django.urls import path, include
from . import views
from rest_framework import routers

# router = routers.DefaultRouter(trailing_slash=False)
# router.register('productsapi',views.ProductsViewSet,basename='productsapi')

urlpatterns = [
    # path('',include(router.urls)),
    path('products/',views.products_view,name='products-list'),
   
]


