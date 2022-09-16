from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from ..constantes import RESET_PASSWORD_MESSAGE, RESET_PASSWORD_SUBJECT, EMAIL_HOST_USER, \
    SET_PASSWORD_SUBJECT, SET_PASSWORD_MESSAGE
from ..models import User, Token, Member, Author, Admin
from ..serializers import UserSerializer, TokenSerializer


class RegisterView(APIView):
    def post(self, request):
        try:
            User.objects.get(email = request.data['email'])
            return Response(data={'message': 'This email already assign to a user, try to log in'},
                            status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            if request.data.get('role_id') == 3:
                member = Member()
                member.user = user
                member.save()
            elif request.data.get('role_id') == 2:
                author = Author()
                author.user = user
                author.save();
            elif request.data.get('role_id') == 1:
                admin = Admin()
                admin.user = user
                admin.save();

            now = datetime.now()
            expires_at = now + timedelta(days=15)
            token = Token()
            token.expire_at = expires_at
            token.user = user
            token.save()
            send_email_to_user(token, False)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


################## TO ADD CUSTOM FIELDS RO JWT #############################
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        #token['date_of_birth'] = str(user.date_of_birth)
        token['email'] = user.email
        token['phone'] = user.phone
        #token['picture'] = user.picture
        token['role']=user.role.role_name
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

################## END TO ADD CUSTOM FIELDS RO JWT #############################

class TokenCreate(CreateAPIView):
    serializer_class = TokenSerializer
    def create(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            user = User.objects.get(email=email);
            now = datetime.now()
            expires_at = now + timedelta(minutes=10)
            token = Token()
            token.expire_at = expires_at
            token.user = user
            token.save()
            # message = RESET_PASSWORD_MESSAGE + str(token.token);
            # send_mail(RESET_PASSWORD_SUBJECT, message, EMAIL_HOST_USER, [email])
            send_email_to_user(token, True)

            return Response(data={"message": "Email with link to reset password have bees successfully sent to user"},
                            status=status.HTTP_200_OK);

        except User.DoesNotExist:
            return Response(data={'message': 'No user found with the given email'}, status=status.HTTP_404_NOT_FOUND);


# def reset_password(self, request):

class ResetPassword(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        password = request.data['password']
        request_token = request.data['token']
        try:
            token = Token.objects.get(token=request_token)
            if timezone.now() > token.expire_at:
                return Response(data={'message': 'Token expired, go to log in page to resend another one'},
                                status=status.HTTP_410_GONE);

            user = token.user
            user.set_password(password)
            token.delete()
            user.save()

            return Response(data={'message': 'Password changed successfully'},
                            status=status.HTTP_200_OK);

        except Token.DoesNotExist:
            return Response(data={'message': 'Token is invalid, double check your inbox'},
                            status=status.HTTP_404_NOT_FOUND);


def send_email_to_user(token: Token, is_reset_password: bool):
        if is_reset_password:
            message = RESET_PASSWORD_MESSAGE + str(token.token);
            send_mail(RESET_PASSWORD_SUBJECT, message, EMAIL_HOST_USER, [token.user.email])
        else:
            message = SET_PASSWORD_MESSAGE + str(token.token);
            send_mail(SET_PASSWORD_SUBJECT, message, EMAIL_HOST_USER, [token.user.email])