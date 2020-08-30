from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
  path('', views.ArticleView.as_view()),
  path('<int:article_pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
  path('<int:article_pk>/bookmark/', views.ArticleBookmarkView.as_view(), name="article_bookmark"),
  path('<int:article_pk>/comment/', views.CommentView.as_view(), name='comment'),
  path('<int:article_pk>/comment/<int:comment_pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
]