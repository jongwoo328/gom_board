from django.urls import path

from . import views


urlpatterns = [
    path('<int:user_id>/', views.UserDetailView.as_view()),
    path('verify/email/', views.verify_email),
    path('verify/username/', views.verify_username),
]