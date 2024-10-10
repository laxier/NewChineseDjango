from rest_framework import serializers
from mindmaps.models import MindMap, ChineseWord, WordInMindMap

class ChineseWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChineseWord
        fields = ['id', 'simplified', 'traditional', 'pinyin', 'meaning']

class WordInMindMapSerializer(serializers.ModelSerializer):
    # Flatten the ChineseWord fields directly
    id = serializers.IntegerField(source='word.id')
    simplified = serializers.CharField(source='word.simplified')
    traditional = serializers.CharField(source='word.traditional')
    pinyin = serializers.CharField(source='word.pinyin')
    meaning = serializers.CharField(source='word.meaning')
    children = serializers.SerializerMethodField()

    class Meta:
        model = WordInMindMap
        fields = ['id', 'simplified', 'traditional', 'pinyin', 'meaning', 'children']

    def get_children(self, obj):
        return WordInMindMapSerializer(obj.children.all(), many=True).data

class MindMapSerializer(serializers.ModelSerializer):
    root_words = serializers.SerializerMethodField()

    class Meta:
        model = MindMap
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'root_words']

    def get_root_words(self, obj):
        # Filter to get only root words (words without a parent)
        root_words = WordInMindMap.objects.filter(mind_map=obj, parent__isnull=True)
        return WordInMindMapSerializer(root_words, many=True).data
