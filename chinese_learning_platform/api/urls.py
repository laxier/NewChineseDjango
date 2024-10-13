from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MindMapViewSet, ChineseWordViewSet, AddWordToMindMapView, DeckPerformanceViewSet, \
    WordPerformanceViewSet, SentenceListCreateView, SentenceRetrieveUpdateDestroyView

router = DefaultRouter()
router.register(r'mindmaps', MindMapViewSet)
router.register(r'words', ChineseWordViewSet)
router.register(r'deck-performance', DeckPerformanceViewSet, basename='deckperformance')
router.register(r'word-performance', WordPerformanceViewSet, basename='word-performance')

urlpatterns = [
    path('', include(router.urls)),
    path('mindmaps/<int:mindmap_id>/add-word/', AddWordToMindMapView.as_view(), name='add-word-to-mindmap'),
    path('word-performance/<int:pk>/correct/', WordPerformanceViewSet.as_view({'post': 'mark_correct'}),
         name='mark-correct'),
    path('word-performance/<int:pk>/incorrect/', WordPerformanceViewSet.as_view({'post': 'mark_incorrect'}),
         name='mark-incorrect'),

    path('sentences/', SentenceListCreateView.as_view(), name='sentence-list-create'),
    path('sentences/<int:pk>/', SentenceRetrieveUpdateDestroyView.as_view(), name='sentence-detail'),
]
