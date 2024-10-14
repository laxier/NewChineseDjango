from rest_framework import serializers
from .models import LexicalExercise

class LexicalExerciseSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = LexicalExercise
        fields = ['id', 'text', 'audio_file', 'children']

    def get_children(self, instance):
        # Serialize only the children that have no further children
        return LexicalExerciseSerializer(instance.children.filter(children__isnull=True), many=True).data

