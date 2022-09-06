'''from django.contrib.auth.models import User
from django.utils.encoding import DjangoUnicodeDecodeError, smart_str
from rest_framework import status, generics, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializers.user_serializers import *
from django.conf import settings
from django.urls import reverse
from api.tasks import send_email_verify
import jwt


@api_view(['GET'])
def api_user_overview(request):
    api_user_urls = {
        'Token auth': 'token/',
        'Token refresh': 'token/refresh/',

        'Registration': 'registration/',
        'Email verify aft reg': 'registration/email-verify/',

        'Reset password': 'request-reset-password/',
        'Check token': 'password-reset/<uidb64>/<token>/',
        'Complete password': 'password_reset_complete/',

        'Update profile data': 'profile/update/'
    }
    return Response(api_user_urls)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            user = User.objects.only('username', 'email')\
                .get(username=user_data['username'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            link = reverse('email-verify')
            abslt_url = f'http://{current_site}{link}?token={str(token)}'
            send_email_verify.delay(url=abslt_url,
                                    user_email=user.email,
                                    username=user.username)

            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class EmailVerify(views.APIView):

    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.only('id').get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'},
                            status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'},
                            status=status.HTTP_400_BAD_REQUEST)


class RequestEmailResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data,
                                           context={'user': user,
                                                    'request': request})

        if serializer.is_valid(raise_exception=True):
            return Response({
                'success': 'We have sent a link to reset your password'},
                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(generics.GenericAPIView):

    def get(self, request, uidb64, token):

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.only('id').get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please '
                                          'request a new one to change password'},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'massage': 'Credentials is Valid',
                             'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is not valid, please '
                                      'request a new one to change password'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordApi(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerlializer

    def patch(self, request):
        serializer = self.serializer_class(
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            return Response({'success': True,
                             'message': 'Password reset success'},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):

    serializer = \
        UserSerializerWithToken(
            data=request.data,
            context={'request': request})

    if serializer.is_valid(raise_exception=True):
        return Response({'message': 'Your profile data was updated'},
                        status=status.HTTP_200_OK)

    return Response(status=status.HTTP_401_UNAUTHORIZED)



'''