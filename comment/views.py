from rest_framework import permissions, viewsets
from rest_framework.generics import get_object_or_404

from comment.models import Comment
from comment.serializers import CommentSerializer
from user.models import User


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ["user", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ["update", "partial_update", "destroy"]:
            queryset = queryset.filter(user=self.request.user.pk)

        return queryset

    def perform_create(self, serializer: CommentSerializer) -> None:
        user = get_object_or_404(User, pk=self.request.user.pk)
        serializer.save(user=user)
