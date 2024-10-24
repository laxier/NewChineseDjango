from django.urls import path, include
from .views import IndexPageView, UserDecksView, AllWordsView, UserWordsView, ReviewWordsView, UserFavoritesView
from .views_deck import DeckDetailView, EditDeckView, ReviewDeckView, TestDeckView, AddDeckView, CreateDeckView, DeleteDeckView

app_name = 'frontend'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('user/<str:username>/decks/', UserDecksView.as_view(), name='user_decks'),
    path('all-words/', AllWordsView.as_view(), name='all_words'),
    path('user-words/', UserWordsView.as_view(), name='user_words'),
    path('review-words/', ReviewWordsView.as_view(), name='review_words'),
    path('user/favorites/', UserFavoritesView.as_view(), name='user_favorites'),

    path('deck/<int:pk>/', DeckDetailView.as_view(), name='deck_detail'),
    path('deck/edit/<int:pk>/', EditDeckView.as_view(), name='edit_deck'),
    path('deck/review/<int:pk>/', ReviewDeckView.as_view(), name='review_deck'),
    path('deck/test/<int:pk>/', TestDeckView.as_view(), name='test_deck'),
    path('deck/add/<int:pk>/', AddDeckView.as_view(), name='add_deck'),
    path('deck/create/', CreateDeckView.as_view(), name='create_deck'),
    path('deck/<int:pk>/delete/', DeleteDeckView.as_view(), name='delete_deck'),
]
