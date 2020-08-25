from rest_framework import serializers

from .models import Article, Comment

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
  class Meta:
    model = Article
    fields = ['id', 'title', 'content', 'parent_article', 'comments']

