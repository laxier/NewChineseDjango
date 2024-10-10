from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MindMapViewSet, CategoryViewSet, ChineseWordViewSet

router = DefaultRouter()
router.register(r'mindmaps', MindMapViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'words', ChineseWordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]