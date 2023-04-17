# Third party imports
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

# Internal imports
from .models import Profile
from followers.models import Follower


class ProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for Profiles.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'city', 'country',
            'name', 'about', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
        ]
