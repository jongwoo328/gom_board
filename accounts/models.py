from django.db import models
from django.contrib.auth.models import AbstractUser

from articles.models import Article


class CustomUser(AbstractUser):
    bookmarked_articles = models.ManyToManyField(
        Article,
        related_name='bookmarked_users'
    )