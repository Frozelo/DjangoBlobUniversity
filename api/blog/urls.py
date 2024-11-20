from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import YourModelViewSet

router = DefaultRouter()
router.register(r'categories', YourModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
