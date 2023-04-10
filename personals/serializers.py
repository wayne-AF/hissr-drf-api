# Third party imports
from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

# Internal imports
from .models import Personal
from likes.models import Like


class PersonalSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for Personals.
    Personals cannot be commented on or liked.
    Users can respond to the poster directly via message.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Personal
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'country', 'city', 'title',
            'content'
        ]
