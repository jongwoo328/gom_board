from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from .serializers import AritcleSerializer
from .models import Article


def index(request):
  return response()

@swagger_auto_schema(method='post', request_body=AritcleSerializer)
@api_view(['POST'])
def article_create(request):
  serializer = AritcleSerializer(data=request.data)
  if serializer.is_valid(raise_exception=True):
    serializer.save(user=request.user, parent_article=None)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def re_article_create(request, aritcle_pk):
  serializer = AritcleSerializer(data=request.data)
  if serializer.is_valid(raise_exception=True):
    serializer.save(user=request.user, parent_article=aritcle_pk)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
@api_view(['GET'])
def detail(request, aritcle_pk):
  article = get_object_or_404(Article, pk=article_pk)
  serializer = AritcleSerializer(article)
  return Response(serializer.data, status=status.HTTP_200_OK)