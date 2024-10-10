from rest_framework import viewsets, status
from rest_framework.response import Response
from mindmaps.models import MindMap, Category, ChineseWord, WordInMindMap
from .serializers import MindMapSerializer, CategorySerializer, ChineseWordSerializer, WordInMindMapSerializer

class MindMapViewSet(viewsets.ModelViewSet):
    queryset = MindMap.objects.all()
    serializer_class = MindMapSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

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

    def perform_create(self, serializer):
        word_in_map = serializer.save()
        category_ids = self.request.data.get('categories', [])
        categories = Category.objects.filter(id__in=category_ids, mind_map=word_in_map.mind_map)
        word_in_map.categories.set(categories)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        category_ids = request.data.get('categories', [])
        if category_ids:
            categories = Category.objects.filter(id__in=category_ids, mind_map=instance.mind_map)
            instance.categories.set(categories)

        return Response(serializer.data)