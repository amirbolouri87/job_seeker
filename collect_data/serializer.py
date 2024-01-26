from rest_framework import serializers


class TranslateEnglishTextSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=5000, required=False)
    is_translated = serializers.BooleanField()
