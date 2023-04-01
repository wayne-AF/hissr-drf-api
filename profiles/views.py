from rest_framework import generics, filters
from django.db.models import Count
from .models import Profile
from .serializers import ProfileSerializer
from hissr_drf_api.permissions import IsOwnerOrReadOnly



class ProfileList(generics.ListAPIView):
    """
    List all profiles. Profile creation is handled by Django signals.
    Distinct=True prevents duplicates from being counted.
    """
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        # show all profiles that are followed by a profile, given its ID
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    The profile owner can retrieve and update the profile.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
