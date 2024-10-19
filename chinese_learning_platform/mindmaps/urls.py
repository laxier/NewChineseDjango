from django.urls import path
from .views import MindMapListView, MindMapDetailView, MindMapCreateView
app_name = 'mindmaps'
urlpatterns = [
    path('', MindMapListView.as_view(), name='mindmap-list'),
    path('<int:pk>/', MindMapDetailView.as_view(), name='mindmap-detail'),
    path('create/', MindMapCreateView.as_view(), name='mindmap-create'),
]
