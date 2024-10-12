# serializers.py
from rest_framework import serializers
from chineseword.models import ChineseWord

class WrongAnswerSerializer(serializers.ModelSerializer):
    pinyin = serializers.CharField(allow_null=True)
    meaning = serializers.CharField(allow_null=True)

    class Meta:
        model = ChineseWord
        fields = ['id', 'simplified', 'pinyin', 'meaning']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['simplified'] = representation.get('simplified', '') or ''
        representation['pinyin'] = representation.get('pinyin', '') or ''
        representation['meaning'] = representation.get('meaning', '') or ''

        return representation
