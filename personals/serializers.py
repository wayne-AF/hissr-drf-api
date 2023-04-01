from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin
from .models import Personal
from likes.models import Like


class PersonalSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Personals/Missed Connections cannot be commented on, only liked.
    Users can respond to the poster directly via message.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    # like_id = serializers.SerializerMethodField()
    # likes_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # def get_like_id(self, obj):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         like = Like.objects.filter(
    #             owner=user, personal=obj
    #         ).first()
    #         return like.id if like else None
    #     return None

    class Meta:
        model = Personal
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'country', 'city', 'title',
            'content',
        ]

        # 'like_id', 'likes_count',
