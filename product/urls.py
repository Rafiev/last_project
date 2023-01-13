from django.urls import include, path
from rest_framework.routers import DefaultRouter

from product.views import CategoryViewSet, ProductViewSet, get_hello

router = DefaultRouter()
router.register('category', CategoryViewSet)
router.register('', ProductViewSet)

urlpatterns = [
    path('hello/', get_hello),
    path('', include(router.urls)),
]