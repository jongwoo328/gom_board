from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bookmarked_articles = models.ManyToManyField(
        'articles.Article',
        related_name='bookmarked_users'
    )