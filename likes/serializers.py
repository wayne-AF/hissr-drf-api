# Third party imports
from rest_framework import serializers
from django.db import IntegrityError

# Internal imports
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Likes.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'personal',]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
