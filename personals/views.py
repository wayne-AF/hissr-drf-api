from rest_framework import generics, permissions, filters
from django.db.models import Count
from .models import Personal
from .serializers import PersonalSerializer
from hissr_drf_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class PersonalList(generics.ListCreateAPIView):
    """
    List Personal/Missed Connection posts or create one if user is logged in.
    """
    serializer_class = PersonalSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Personal.objects.all()

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
