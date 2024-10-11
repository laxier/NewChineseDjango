from django.urls import path
from .views import IndexPageView, UserDecksView, AllWordsView, UserWordsView

app_name = 'frontend'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('user/<str:username>/decks/', UserDecksView.as_view(), name='user_decks'),
    path('all-words/', AllWordsView.as_view(), name='all-words'),
    path('user-words/', UserWordsView.as_view(), name='user-words'),
]
