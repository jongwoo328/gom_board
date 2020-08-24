from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Article(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  parent_article = models.ForeignKey('self', on_delete=models.CASCADE)
  title = models.CharField(max_length=30)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  liked_user = models.ManyToManyField(User, related_name='liked_article')

class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  parent_comment = models.ForeignKey('self', on_delete=models.CASCADE)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  liked_user = models.ManyToManyField(User, related_name='liked_comment')