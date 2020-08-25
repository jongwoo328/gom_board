from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


User = get_user_model()

class UserDetailView(APIView):

    permission_classes = (
        IsAuthenticated,
    )
    def get_object(self, user_id):
        return get_object_or_404(User, pk=user_id)

    def delete(self, request, user_id):
        if request.user.id == user_id:
            user = self.get_object(user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)