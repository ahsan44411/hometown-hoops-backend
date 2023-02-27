import jwt
import random
import string
from accounts.models import Jwt
from datetime import datetime, timedelta
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from hometown_hoops_backend import settings
from rest_framework.response import Response
from django.utils.encoding import force_bytes
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import RegisterSerializer, LoginSerializer, CustomUserSerializer

# Create your views here.

User = get_user_model()


def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    return jwt.encode(
        {'exp': datetime.now() + timedelta(days=30), **payload},
        settings.SECRET_KEY,
        algorithm='HS256'
    )


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user_serializer = self.serializer_class(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        if type(user) is str:
            return Response({'error': user}, status=400)

        Jwt.objects.filter(user_id=user.id).delete()

        access = get_access_token({'user_id': user.id})

        Jwt.objects.create(
            user_id=user.id, access=access
        )
        return Response({"access_token": access, 'user': CustomUserSerializer(user).data})


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if not user:
            return Response({'error': 'Invalid email or password'}, status="400")
        # delete previous if any
        Jwt.objects.filter(user_id=user.id).delete()

        access = get_access_token({'user_id': user.id})
        # create new
        Jwt.objects.create(
            user_id=user.id, access=access
        )
        return Response({"access_token": access, 'user': CustomUserSerializer(user).data})


class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def send_change_password_email(self, email):

        context = {
            'domain': '',
            'endpoint': 'confirm-change-password/',
            'email': urlsafe_base64_encode(force_bytes(email)),
        }

        email_template = "accounts/change-password-link.html"

        email_template = get_template(email_template)

        email_template = email_template.render(context)

        msg = EmailMessage(
            'Finqube || Change Password',
            email_template,
            "noreply@finqube.io",
            [email, ]
        )

        msg.content_subtype = "html"

        msg.send()

    def get(self, request):
        try:
            self.send_change_password_email(request.user.email)
            return Response({'message': 'Reset password link sent to your email'}, status=200)
        except Exception as e:
            print(e)
            return Response({'message': 'Could not send reset password link, Please try again'}, status=400)


class ConfirmChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            if not User.objects.filter(email=data['email']).exists():
                return Response({'error': 'Email not associated with any account'}, status=400)

            user = User.objects.get(email=data['email'])

            user.set_password(data['password1'])

            user.save()

            context = {}

            email_template = "accounts/confirm-password-change.html"

            email_template = get_template(email_template)

            email_template = email_template.render(context)

            msg = EmailMessage(
                'Hometown hoops || Password Changed',
                email_template,
                "ahsan44411@gmail.com",
                [data['email'], ]
            )

            msg.content_subtype = "html"

            msg.send()

            return Response({'message': 'Password reset successfully'}, status=200)
        except Exception as e:
            return Response({'error': 'Unable to change password, please contact customer support'}, status=200)


class LoadUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        return Response({'user': CustomUserSerializer(user).data})
