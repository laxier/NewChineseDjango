from django.urls import path
from .views import ChineseWordDetailView
from .views import HSK4ProgressDownloadView

app_name = 'wordpages'

urlpatterns = [
    path('<int:pk>/', ChineseWordDetailView.as_view(), name='chinese_word_detail'),
    path('download-hsk4-progress/', HSK4ProgressDownloadView.as_view(), name='download_hsk4_progress'),
]

