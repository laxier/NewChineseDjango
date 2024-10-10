from rest_framework import serializers
from mindmaps.models import MindMap, Category, ChineseWord, WordInMindMap

class ChineseWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChineseWord
        fields = ['id', 'simplified', 'traditional', 'pinyin', 'meaning']

class WordInMindMapSerializer(serializers.ModelSerializer):
    word = ChineseWordSerializer(read_only=True)
    word_id = serializers.PrimaryKeyRelatedField(queryset=ChineseWord.objects.all(), source='word', write_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = WordInMindMap
        fields = ['id', 'word_id', 'word', 'children']

    def get_children(self, obj):
        # Recursively serialize the children of the current node
        return WordInMindMapSerializer(obj.children.all(), many=True).data

class CategorySerializer(serializers.ModelSerializer):
    words = WordInMindMapSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'mind_map', 'words']

class MindMapSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    root_words = serializers.SerializerMethodField()

    class Meta:
        model = MindMap
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'root_words']

    def get_root_words(self, obj):
        root_words = WordInMindMap.objects.filter(mind_map=obj, parent=None)
        return WordInMindMapSerializer(root_words, many=True).data
