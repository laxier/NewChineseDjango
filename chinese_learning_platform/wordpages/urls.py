from django.urls import path
from .views import ChineseWordDetailView

urlpatterns = [
    path('<int:pk>/', ChineseWordDetailView.as_view(), name='chinese_word_detail'),
]