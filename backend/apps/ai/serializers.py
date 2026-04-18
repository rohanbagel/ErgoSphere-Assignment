from rest_framework import serializers


class AskRequestSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=2000)
    book_id = serializers.IntegerField(required=False, allow_null=True)
    top_k = serializers.IntegerField(required=False, min_value=1, max_value=10, default=5)
