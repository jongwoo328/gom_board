from rest_framework import serializers
from .models import Article, Comment

class AritcleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Article
    fields = ['title', 'content',]