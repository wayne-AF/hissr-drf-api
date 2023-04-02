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
    List Personal/Missed Connection posts or create one if user is logged in.
    Users cannot like or comment on Missed Connection posts, so users cannot
    filter posts by likes or comments.
    """
    serializer_class = PersonalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Personal.objects.all()
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
        'country',
        'city'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PersonalDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    User can retrieve a Missed Connections post and edit or delete
    it if they own it.
    """
    serializer_class = PersonalSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Personal.objects.all()
