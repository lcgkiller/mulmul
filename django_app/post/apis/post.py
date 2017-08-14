from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models.others import Tag
from utils import ObjectIsRequestUser
from ..serializers import PostSerializer
from ..models import Post

__all__ = (
    'PostListCreateView',
    'PostDetailView',
    'PostLikeToggleView',
    'PostSearchView',
    'HashtagPostListView',
)


class PostListCreateView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_pk):
        post = self.get_object(post_pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_pk):
        post = self.get_object(post_pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk):
        post = self.get_object(post_pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeToggleView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

    def get_object(self, post_pk):
        try:
            return Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_pk):
        post = self.get_object(post_pk)
        post_like, post_like_created = post.postlike_set.get_or_create(
            user=request.user
        )
        if not post_like_created:
            post_like.delete()
        return Response({'created': post_like_created})


class PostSearchView(APIView):
    pass


class HashtagPostListView(APIView):

    def get_object(self, tag_name):
        try:
            return Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, tag_name):
        tag = self.get_object(tag_name)
        posts = Post.objects.filter(comment__tags=tag)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)