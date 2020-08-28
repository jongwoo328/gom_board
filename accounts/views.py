from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import EmailVerifySerializer, UsernameVerifySerializer


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


@swagger_auto_schema(method='post', request_body=EmailVerifySerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    email = request.data.get('email', None)
    if email:
        result = {
            'valid': not User.objects.filter(email=email).exists(),
            'email': email
        }
        return Response(result, status=status.HTTP_200_OK)
    result = {
        'detail': 'email 정보가 필요합니다.'
    }
    return Response(result, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=UsernameVerifySerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_username(request):
    username = request.data.get('username', None)
    if username:
        result = {
            'valid' : not User.objects.filter(username=username).exists(),
            'username': username
        }
        return Response(result, status=status.HTTP_200_OK)
    result = {
        'detail': 'username 정보가 필요합니다.'
    }
    return Response(result, status=status.HTTP_400_BAD_REQUEST)