from rest_framework import serializers
from .models import LexicalExercise

class LexicalExerciseSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = LexicalExercise
        fields = ['id', 'text', 'audio_file', 'children']

    def get_children(self, instance):
        """
        Получает дочерние элементы из предзагруженных данных
        """
        if hasattr(instance, '_prefetched_children'):
            return LexicalExerciseSerializer(
                instance._prefetched_children,
                many=True
            ).data
        return []

