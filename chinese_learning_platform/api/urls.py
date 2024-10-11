from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MindMapViewSet, ChineseWordViewSet, AddWordToMindMapView

router = DefaultRouter()
router.register(r'mindmaps', MindMapViewSet)
router.register(r'words', ChineseWordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('mindmaps/<int:mindmap_id>/add-word/', AddWordToMindMapView.as_view(), name='add-word-to-mindmap'),


]
