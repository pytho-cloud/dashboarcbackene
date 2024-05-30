# serializers.py

from rest_framework import serializers
from datetime import datetime

class UserModelSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    created_at = serializers.DateTimeField(default=datetime.now)
    roll = serializers.CharField(max_length=50)
    img = serializers.CharField(required=False)

    def create(self, validated_data):
        return validated_data
