from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from .serializers import ArticleSerializer, CommentSerializer


class ArticleView(APIView):

  @swagger_auto_schema(request_body=ArticleSerializer)
  def post(self, request):
    """
        # Article을 작성하는 요청
        ---
        ## 내용
            - ssss: zzz
            - zzzz : ddd
     
    """
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailView(APIView):

  def get_object(self, article_pk):
    return get_object_or_404(Article, pk=article_pk)
  
  def delete(self, request, article_pk):
    article = self.get_object(article_pk)
    article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  def get(self, resquest, article_pk):
    article = self.get_object(article_pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def patch(self, request, article_pk):
    article = self.get_object(article_pk)
    serializer = ArticleSerializer(instance=article, data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CommentView(APIView):
  
  def get(self, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comment.objects.all()
    print(comments)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer, status=status.HTTP_200_OK)

  def post(self, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user, article=article)
      return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):

  def get_object(self, comment_pk):
    return get_object_or_404(Comment, pk=comment_pk)
  
  # don't use this function
  def patch(self, request, comment_pk):
    comment = self.get_object(comment_pk)
    serializer = CommentSerializer(instance=comment, data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    
  def delete(self, request, comment_pk):
    comment = self.get_object(comment_pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)