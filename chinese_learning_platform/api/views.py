from rest_framework import viewsets, status
from rest_framework.response import Response
from mindmaps.models import MindMap, ChineseWord, WordInMindMap
from .serializers import MindMapSerializer, ChineseWordSerializer, WordInMindMapSerializer, AddWordSerializer
from rest_framework.views import APIView

class MindMapViewSet(viewsets.ModelViewSet):
    queryset = MindMap.objects.all()
    serializer_class = MindMapSerializer

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

            # Create or get the ChineseWord
            chinese_word, created = ChineseWord.objects.get_or_create(simplified=simplified)

            # Get the MindMap
            try:
                mind_map = MindMap.objects.get(id=mindmap_id)
            except MindMap.DoesNotExist:
                return Response({"error": "MindMap not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if WordInMindMap already exists
            word_in_mind_map, created = WordInMindMap.objects.get_or_create(word=chinese_word, mind_map=mind_map)

            # Handle parent associations
            if parent_character:
                try:
                    # Assuming parent_character is the simplified character of a ChineseWord
                    parent_word = ChineseWord.objects.get(simplified=parent_character)
                    # Get the parent WordInMindMap entry based on the parent ChineseWord
                    parent_word_in_map = WordInMindMap.objects.get(word=parent_word, mind_map=mind_map)
                    word_in_mind_map.parent = parent_word_in_map  # Associate with the WordInMindMap entry
                    word_in_mind_map.save()
                except ChineseWord.DoesNotExist:
                    return Response({"error": f"Parent word '{parent_character}' not found"}, status=status.HTTP_404_NOT_FOUND)
                except WordInMindMap.DoesNotExist:
                    return Response({"error": f"Parent word '{parent_character}' not found in the MindMap"}, status=status.HTTP_404_NOT_FOUND)

            # Handle children associations
            for child_char in child_characters:
                try:
                    # Create or get the child ChineseWord
                    child_word, _ = ChineseWord.objects.get_or_create(simplified=child_char)
                    # Get or create WordInMindMap entry for the child
                    child_word_in_map, _ = WordInMindMap.objects.get_or_create(word=child_word, mind_map=mind_map)
                    child_word_in_map.parent = word_in_mind_map  # Set the parent for the child
                    child_word_in_map.save()
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Word and children added successfully", "word_id": word_in_mind_map.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
