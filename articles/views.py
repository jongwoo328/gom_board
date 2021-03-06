from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser

from drf_yasg.utils import swagger_auto_schema

from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleCreateSerializer, CommentSerializer, CommentCreateSerializer
from .permissions import ArticleViewPermission
from accounts.serializers import UserBookmarkSerializer


article_per_page = 10

class ArticleView(APIView):

  permission_classes =[ArticleViewPermission]

  @swagger_auto_schema(request_body=ArticleCreateSerializer)
  def post(self, request):
    """
        # Article을 작성하는 요청
    """
    serializer = ArticleCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def get(self, request):
    page = int(request.GET.get('page', 1))
    start_index = article_per_page*(page-1)
    queryset = reversed(Article.objects.filter(parent_article=None)[start_index:start_index + article_per_page ])
    total_article_count = Article.objects.count()
    serializer = ArticleSerializer(instance=queryset, many=True)
    response = {
      'articles': serializer.data,
      'totalArticleCount': total_article_count
    }
    return Response(response, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):

  permission_classes = [ArticleViewPermission]

  def get_object(self, article_pk):
    return get_object_or_404(Article, pk=article_pk)
  
  def delete(self, request, article_pk):
    article = self.get_object(article_pk)
    article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  def get(self, request, article_pk):
    article = self.get_object(article_pk)
    serializer = ArticleSerializer(article)

    if request.user == AnonymousUser():
      count = 0
      is_bookmarked = False
    else:
      count = len(request.user.bookmarked_articles.values())
      is_bookmarked = request.user.bookmarked_articles.filter(id=article_pk).exists()
    res = {
      'data': serializer.data, 
      'bookmark_count': count,
      'is_bookmarked': is_bookmarked
      }
    return Response(res, status=status.HTTP_200_OK)
  
  @swagger_auto_schema(request_body=ArticleCreateSerializer)
  def patch(self, request, article_pk):
    article = self.get_object(article_pk)
    serializer = ArticleCreateSerializer(instance=article, data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleBookmarkView(APIView):

  def get_object(self, article_pk):
    return get_object_or_404(Article, pk=article_pk)

  def post(self, request, article_pk):
    user = request.user
    article = self.get_object(article_pk)
    if user.bookmarked_articles.filter(id=article_pk).exists():
      fake_count = -1
      user.bookmarked_articles.remove(article)
    else:
      fake_count = 1
      user.bookmarked_articles.add(article)
    return Response(fake_count, status=status.HTTP_200_OK)

class CommentView(APIView):

  def get(self, request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comments.filter(parent_comment = None)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(request_body=CommentCreateSerializer)
  def post(self, request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user, article=article)
      return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):

  def get_object(self, comment_pk):
    return get_object_or_404(Comment, pk=comment_pk)

  @swagger_auto_schema(request_body=CommentCreateSerializer)
  def post(self, request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = self.get_object(comment_pk)
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user, article=article, parent_comment=comment)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

  # don't use this function.
  @swagger_auto_schema(request_body=CommentSerializer)
  def patch(self, request, article_pk, comment_pk):
    comment = self.get_object(comment_pk)
    serializer = CommentSerializer(instance=comment, data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    
  def delete(self, request, article_pk, comment_pk):
    comment = self.get_object(comment_pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)