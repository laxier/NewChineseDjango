from rest_framework import serializers
from mindmaps.models import MindMap, WordInMindMap
from chineseword.models import ChineseWord


class ChineseWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChineseWord
        fields = ['id', 'simplified', 'traditional', 'pinyin', 'meaning']

class WordInMindMapSerializer(serializers.ModelSerializer):
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
        # Only return children if there are any
        children = WordInMindMap.objects.filter(parent=obj)
        if children.exists():
            return WordInMindMapSerializer(children, many=True).data
        return None  # Return None instead of an empty list

class MindMapSerializer(serializers.ModelSerializer):
    root_words = serializers.SerializerMethodField()

    class Meta:
        model = MindMap
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'root_words']

    def get_root_words(self, obj):
        # Filter to get only root words (words without a parent)
        root_words = WordInMindMap.objects.filter(mind_map=obj, parent__isnull=True)
        return WordInMindMapSerializer(root_words, many=True).data


class AddWordSerializer(serializers.Serializer):
    simplified = serializers.CharField(max_length=50)
    parent = serializers.CharField(max_length=50, required=False)
    children = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )

from rest_framework import serializers
from users.models import DeckPerformance
from chineseword.models import ChineseWord  # Make sure to import your models


class DeckPerformanceSerializer(serializers.ModelSerializer):
    wrong_answers = serializers.PrimaryKeyRelatedField(queryset=ChineseWord.objects.all(), many=True)

    class Meta:
        model = DeckPerformance
        fields = ['id', 'deck', 'percent_correct', 'wrong_answers']  # Include other fields as needed

    def create(self, validated_data):
        wrong_answers_data = validated_data.pop('wrong_answers')
        deck_performance = DeckPerformance.objects.create(**validated_data)

        # Create the many-to-many relationship
        deck_performance.wrong_answers.set(wrong_answers_data)  # Set the wrong answers directly

        return deck_performance




from users.models import WordPerformance
class WordPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordPerformance
        fields = ['id', 'user', 'word', 'ef_factor', 'repetitions', 'right', 'wrong', 'timestamp', 'edited', 'next_review_date']
        read_only_fields = ['id', 'user', 'timestamp', 'edited', 'next_review_date']

    def create(self, validated_data):
        return WordPerformance.objects.create(**validated_data)