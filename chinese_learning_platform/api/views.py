from rest_framework import viewsets, status
from rest_framework.response import Response
from mindmaps.models import MindMap, ChineseWord, WordInMindMap
from users.models import DeckPerformance, UserDeck, WordPerformance
from .serializers import DeckPerformanceSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import MindMapSerializer, ChineseWordSerializer, WordInMindMapSerializer, AddWordSerializer, \
    WordPerformanceSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import SessionAuthentication
from django.core.exceptions import MultipleObjectsReturned


class DeckPerformanceViewSet(viewsets.ModelViewSet):
    queryset = DeckPerformance.objects.all()
    serializer_class = DeckPerformanceSerializer
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        print("Received data:", self.request.data)
        deck = serializer.validated_data.get('deck')
        if not UserDeck.objects.filter(user=self.request.user, deck=deck).exists():
            raise PermissionDenied("You can only create performance records for your own decks.")

        # Save the deck performance; wrong_answers are handled in the serializer
        deck_performance = serializer.save(user=self.request.user)

        user_deck = get_object_or_404(UserDeck, user=self.request.user, deck=deck_performance.deck)
        user_deck.percent = deck_performance.percent_correct
        user_deck.save()


class WordPerformanceViewSet(viewsets.ModelViewSet):
    queryset = WordPerformance.objects.all()
    serializer_class = WordPerformanceSerializer
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update_performance(self, request, pk, correct=True):
        performance = self.get_object()
        if performance.user != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        if correct:
            performance.correct()
        else:
            performance.incorrect()
        performance.save()
        serializer = self.get_serializer(performance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def mark_correct(self, request, pk):
        return self.update_performance(request, pk, correct=True)

    def mark_incorrect(self, request, pk):
        return self.update_performance(request, pk, correct=False)


class MindMapViewSet(viewsets.ModelViewSet):
    queryset = MindMap.objects.all()
    serializer_class = MindMapSerializer
    permission_classes = []


class ChineseWordViewSet(viewsets.ModelViewSet):
    queryset = ChineseWord.objects.all()
    serializer_class = ChineseWordSerializer


class WordInMindMapViewSet(viewsets.ModelViewSet):
    queryset = WordInMindMap.objects.all()
    serializer_class = WordInMindMapSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class AddWordToMindMapView(APIView):

    def post(self, request, mindmap_id):
        serializer = AddWordSerializer(data=request.data)
        if serializer.is_valid():
            simplified = serializer.validated_data['simplified']
            parent_character = serializer.validated_data.get('parent')  # Expecting a single parent character
            child_characters = serializer.validated_data.get('children', [])  # Accepting a list of child characters

            chinese_word = self.get_or_create_chinese_word(simplified)
            mind_map = self.get_mind_map_or_404(mindmap_id)

            word_in_mind_map = self.get_or_create_word_in_map(chinese_word, mind_map)

            if parent_character:
                parent_word_in_map = self.handle_parent_association(parent_character, mind_map)
                word_in_mind_map.parent = parent_word_in_map
                word_in_mind_map.save()

            self.handle_children_associations(child_characters, word_in_mind_map, mind_map)

            return Response(
                {"message": "Word and children added successfully", "word_id": word_in_mind_map.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_or_create_chinese_word(self, simplified):
        """Create or get a ChineseWord by its simplified form."""
        chinese_word, _ = ChineseWord.objects.get_or_create(simplified=simplified)
        return chinese_word

    def get_mind_map_or_404(self, mindmap_id):
        """Get a MindMap by its ID or return 404 response."""
        try:
            return MindMap.objects.get(id=mindmap_id)
        except MindMap.DoesNotExist:
            raise Response({"error": "MindMap not found"}, status=status.HTTP_404_NOT_FOUND)

    def get_or_create_word_in_map(self, chinese_word, mind_map):
        """Create or get a WordInMindMap entry."""
        word_in_mind_map, _ = WordInMindMap.objects.get_or_create(word=chinese_word, mind_map=mind_map)
        return word_in_mind_map

    def handle_parent_association(self, parent_character, mind_map):
        """Handle association with a parent word in the MindMap."""
        try:
            parent_word = ChineseWord.objects.get(simplified=parent_character)
            parent_word_in_map = WordInMindMap.objects.get(word=parent_word, mind_map=mind_map)
            return parent_word_in_map
        except ChineseWord.DoesNotExist:
            raise Response({"error": f"Parent word '{parent_character}' not found"}, status=status.HTTP_404_NOT_FOUND)
        except WordInMindMap.DoesNotExist:
            raise Response({"error": f"Parent word '{parent_character}' not found in the MindMap"},
                           status=status.HTTP_404_NOT_FOUND)

    def handle_children_associations(self, child_characters, word_in_mind_map, mind_map):
        """Handle associations of child words in the MindMap."""
        for child_char in child_characters:
            try:
                child_word = self.get_or_create_chinese_word(child_char)
                child_word_in_map = self.get_or_create_word_in_map(child_word, mind_map)
                child_word_in_map.parent = word_in_mind_map  # Set the parent for the child
                child_word_in_map.save()
            except Exception as e:
                raise Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from wordpages.models import Sentence
from .serializers import SentenceSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics


class SentenceListCreateView(generics.ListCreateAPIView):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SentenceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


from .serializers import ChineseWordFavoriteSerializer

class ChineseWordFavoriteView(generics.UpdateAPIView):
    queryset = ChineseWord.objects.all()
    serializer_class = ChineseWordFavoriteSerializer


    def perform_update(self, serializer):
        serializer.update(serializer.instance, {'user': self.request.user})

class ChineseWordFavoriteStatusView(APIView):

    def get(self, request, word_id):
        try:
            word = ChineseWord.objects.get(id=word_id)
            is_favorite = request.user in word.favorites.all()
            return Response({'is_favorite': is_favorite})
        except ChineseWord.DoesNotExist:
            return Response({'error': 'Word not found'}, status=404)