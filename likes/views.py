# Third party imports
from rest_framework import generics, permissions

# Internal imports
from hissr_drf_api.permissions import IsOwnerOrReadOnly
from .models import Like
from .serializers import LikeSerializer


class LikeList(generics.ListCreateAPIView):
    """
    Displays list of likes or create a like.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like or delete a like if owned by user.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
