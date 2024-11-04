from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """Получение данных авторизованного пользователя (кроме пароля)"""
    def get(self, request):
        user_id = request.user.id
        user = User.objects.filter(id=user_id).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

