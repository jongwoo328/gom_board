from rest_framework import serializers

from .models import Article, Comment
from accounts.serializers import UserSerializer, UserBookmarkSerializer


class CommentSerializer(serializers.ModelSerializer):
  child_comments = serializers.SerializerMethodField()
  user = UserSerializer()
  class Meta:
    model = Comment
    fields = ['id', 'user', 'content', 'parent_comment', 'child_comments']
  
  def get_child_comments(self, instance):
    from .serializers import CommentSerializer
    return CommentSerializer(instance.child_comments, many=True).data


class CommentCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['content']


class ArticleSerializer(serializers.ModelSerializer):
  comments = serializers.SerializerMethodField()
  child_articles = serializers.SerializerMethodField()
  user = UserBookmarkSerializer()
  class Meta:
    model = Article
    fields = ['id', 'title', 'content', 'parent_article', 'comments', 'child_articles', 'user', 'created_at', 'liked_user']

  def get_child_articles(self, instance):
    from .serializers import ArticleSerializer
    return ArticleSerializer(instance.child_articles, many=True).data

  def get_comments(self, instance):
    qs = Comment.objects.filter(article=instance, parent_comment=None)
    return CommentSerializer(instance=qs, many=True).data


class ArticleCreateSerializer(serializers.ModelSerializer):
  id = serializers.IntegerField(required=False)
  class Meta:
    model = Article
    fields = ['id', 'title', 'content']