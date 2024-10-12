from django.urls import path, include
from .views import IndexPageView, UserDecksView, AllWordsView, UserWordsView, ReviewWordsView
from .views_deck import DeckDetailView, EditDeckView, ReviewDeckView, TestDeckView, AddDeckView

app_name = 'frontend'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('user/<str:username>/decks/', UserDecksView.as_view(), name='user_decks'),
    path('all-words/', AllWordsView.as_view(), name='all-words'),
    path('user-words/', UserWordsView.as_view(), name='user-words'),
    path('review-words/', ReviewWordsView.as_view(), name='review_words'),

    path('deck/<int:pk>/', DeckDetailView.as_view(), name='deck_detail'),
    path('deck/edit/<int:pk>/', EditDeckView.as_view(), name='edit_deck'),
    path('deck/review/<int:pk>/', ReviewDeckView.as_view(), name='review_deck'),
    path('deck/test/<int:pk>/', TestDeckView.as_view(), name='test_deck'),
    path('deck/add/<int:pk>/', AddDeckView.as_view(), name='add_deck'),

    path('word/', include('wordpages.urls'))
]
