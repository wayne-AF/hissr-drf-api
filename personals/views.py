# Third party imports
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

# Internal imports
from hissr_drf_api.permissions import IsOwnerOrReadOnly
from .serializers import PersonalSerializer
from .models import Personal


class PersonalList(generics.ListCreateAPIView):
    """
    List Personal posts or create one if user is logged in.
    """
    serializer_class = PersonalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Personal.objects.annotate(
        likes_count=Count('likes', distinct=True),
        # comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'owner__profile',
        'likes__owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
        'category',
    ]
    ordering_fields = [
        'likes_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PersonalDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    User can retrieve a Personal and edit or delete
    it if they own it.
    """
    serializer_class = PersonalSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Personal.objects.annotate(
        likes_count=Count('likes', distinct=True),
        # comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
