from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import User
from . import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .renderers import UserRender
from .serializers import UserCreationSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, LogoutSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from  django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class HelloAuthView(generics.GenericAPIView):

    @swagger_auto_schema(operation_description="Hello Auth")
    def get(self, request):
        return Response(data={"message": "Hello Auth"}, status=status.HTTP_200_OK)


class UserCreationView(generics.GenericAPIView):
    serializer_class = serializers.UserCreationSerializer
    renderer_classes = (UserRender,)

    @swagger_auto_schema(operation_description="Create a user account")
    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = UserCreationSerializer

    @swagger_auto_schema(
        operation_summary="Generate JWT pair",
        operaion_description ="This login a user with email and password"
    )

    def post(self, request:Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            response ={
                "message":"Login Successful",
                "token": user.auth_token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message":"Invalid email or password"})


    @swagger_auto_schema(
        operation_summary="Get request info",
        operaion_description ="This shows the request info"
    )

    def get(self, request:Request):
        content={
            "user": str(request.user),
            "auth":str(request.auth)
        }

        return Response(data=content, status=status.HTTP_200_OK)




    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello, \n  Use link below to reset  your password \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your Password'}

            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id =smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            return Response({'success': True, 'message':'Credentials Valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, Please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, Please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def path(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':'Password reset successfully'}, status=status.HTTP_200_OK)



class LogoutAPIView(generics.GenericAPIView):
    serializer_class =  LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
         serializer = self.serializer_class(data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()

         return Response(status=status.HTTP_204_NO_CONTENT)





class AuthUserAPIView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(pk=request.user.pk.pk.pj)
        serializer = UserCreationSerializer(user)
        return Response(serializer.data)



