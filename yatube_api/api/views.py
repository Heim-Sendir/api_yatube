from django.shortcuts import get_object_or_404
from rest_framework import viewsets
# from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
# from rest_framework import mixins
from rest_framework import status


from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # def check_user(self, serializer):
    #     if self.request.user != serializer.data.author:
    #         return Response(status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied('Вы не можете изменять этот пост')
        serializer.save(author=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied('Вы не можете изменять этот пост')
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Пост успешно удалён!"},
                        status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied('Вы не можете удалять этот пост')
        instance.delete()


class GroupRetrieveViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def __get_post(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post

    def get_queryset(self):
        new_queryset = self.__get_post().comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post = self.__get_post()
        serializer.save(author=self.request.user, post=post)
