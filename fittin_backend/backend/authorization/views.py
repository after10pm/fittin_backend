from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from social_django.views import complete
from user.models import User
from user.serializers import UserSerializer


class RegisterView(APIView):
    """Регистрация нового пользователя"""

    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.FORMAT_EMAIL,
                                        description='Email пользователя (обязательное поле)'),
                'password': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='Пароль пользователя(обязательное поле)'),
            },
        )
    )
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Пользователь с данным e-mail уже зарегистрирован.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({'error': 'Пользователь не найден'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Неправильный пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'name': user.name,
            })
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            response = Response(token, status=status.HTTP_200_OK)
            response.set_cookie(key="jwt_token", value=str(token['access']), httponly=True)
            return response
        except TokenError as token_error:
            return Response({'error': str(token_error)}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt_token')
        response.data = {
            'message': 'success'
        }
        return response


class CodeGenerationView(APIView):
    def get(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        code = get_random_string(length=5)
        user.code = code
        user.code_expires = timezone.now() + timezone.timedelta(minutes=10)
        user.save()

        send_mail(
            'Восстановление пароля',
            f'Код для сброса пароля: {code}. Он действителен в течение 10 минут.',
            'fittinbackend@yandex.ru',
            [email],
            fail_silently=False
        )
        return Response({'message': 'Код отправлен на email. Он действителен в течение 10 минут.'},
                        status=status.HTTP_200_OK)


class CodeVerificationView(APIView):
    def post(self, request):
        email = request.data['email']
        code = request.data['code']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        code_expires = user.code_expires
        if code_expires < timezone.now():
            user.code = ''
            user.save()
            return Response({'message': 'Срок действия кода истёк'}, status=status.HTTP_400_BAD_REQUEST)
        if code != user.code:
            return Response({'message': 'Неверный код восстановления'}, status=status.HTTP_400_BAD_REQUEST)
        user.code = 'true'
        user.save()
        return Response({'message': 'Код прошёл проверку'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        if user.code == 'true' and user.code_expires > timezone.now():
            user.code = ''
            user.code_expires = None
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Пароль изменён'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Код не был подтверждён из-за того, что вы ввели неверный код или истекло время'
                                        ' его хранения'}, status=status.HTTP_400_BAD_REQUEST)


class VKLoginView(APIView):
    def get(self, request):
        return redirect('social:begin', 'vk')


class VKAuthCompleteView(APIView):
    def get(self, request):
        user = complete(request, 'vk')
        email = user.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Пользователь с данным e-mail уже зарегистрирован.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
