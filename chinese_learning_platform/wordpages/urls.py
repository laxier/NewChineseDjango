from django.urls import path
from .views import ChineseWordDetailView
app_name='wordpages'

urlpatterns = [
    path('<int:pk>/', ChineseWordDetailView.as_view(), name='chinese_word_detail'),
]