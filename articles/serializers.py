from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Article
    fields = ['title', 'content', 'parent_article']

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['content', 'parent_comment']