from rest_framework import serializers

from .models import Article, Comment
from accounts.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
  child_comments = serializers.SerializerMethodField()
  class Meta:
    model = Comment
    fields = ['id', 'content', 'parent_comment', 'child_comments']
  
  def get_child_comments(self, instance):
    from .serializers import CommentSerializer
    return CommentSerializer(instance.child_comments, many=True).data

class ArticleSerializer(serializers.ModelSerializer):
  comments = CommentSerializer(many=True)
  child_articles = serializers.SerializerMethodField()
  user = UserSerializer()
  class Meta:
    model = Article
    fields = ['id', 'title', 'content', 'parent_article', 'comments', 'child_articles', 'user', 'created_at', 'liked_user']

  def get_child_articles(self, instance):
    from .serializers import ArticleSerializer
    return ArticleSerializer(instance.child_articles, many=True).data

class ArticleCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Article
    fields = ['title', 'content']