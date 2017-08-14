from django.db.models import Q
from django.http import Http404
from rest_framework import permissions, generics, filters
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import ObjectIsRequestUser
from ..serializers import PostSerializer
from ..models import Post

__all__ = (
    'PostListCreateView',
    'PostDetailView',
    'PostLikeToggleView',
    'PostSearchView',
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


class PostSearchView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter, )

    # '^' : Starts-with search
    # '=' : Exact matches
    # '@' : Full-text search (Only Supported Django's MySQL Backend)
    # '$' : Regex search
    search_fields = ('title', 'content')
    lookup_url_kwarg = "search"

    def get_queryset(self):
        queryset = Post.objects.all()
        keyword = self.request.GET.get('keyword', None)
        if keyword is not None:
            queryset = queryset.filter(
                Q(title__icontains=keyword) |
                Q(content__icontains=keyword)
            )
        return queryset
