from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import UserRegisterSerializer, EmailVerifySerializer
from rest_framework.response import Response
from rest_framework import status
from users.models import User

class UserCreateView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        return Response(
            {
                "message": "Для успешной регистрации осталось подтвердить почту!",
                "email": user.email
            },
            status=status.HTTP_201_CREATED
        )
        
class VerifyEmailView(APIView):
    def post(self, request):
        serializer = EmailVerifySerializer(data=request.data)
        
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        
        user = User.objects.filter(email=email).first()
        if not user:
            raise Response(
                {'error': "Пользователь с таким email не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        if not user.is_code_valid(code):
            return Response(
                {"error": "Неверный или истекший код подтверждения"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.is_active = True
        user.verification_code = None
        user.code_created_at = None
        user.save(update_fields=['is_active', 'verification_code', 'code_created_at'])
        
        return Response(
            {"message": "Email успешно подтвержден. Теперь вы можете войти в аккаунт."}, 
            status=status.HTTP_200_OK
        )
        
        
        
