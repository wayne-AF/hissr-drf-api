# Third party imports
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

# Internal imports
from .models import Post
from likes.models import Like


class PostSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for Posts.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    comments_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content',
            'comments_count', 'city', 'country'
        ]
