import os

from django.shortcuts import render
import hashlib
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics
import random,string
from rest_framework import status


class Usersignup(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                salt = os.urandom(16)
                # salt = "".join(random.choices(string.digits+string.ascii_letters+string.punctuation,k=9))#+"".join(random.choices(string.ascii_letters,k=3))+"".join(random.choices(string.punctuation,k=3))
                pswd = request.data['password']
                serializer.validated_data['password'] = hashlib.sha256(salt+pswd.encode('utf-8')).hexdigest()
                serializer.validated_data['salt'] = salt.hex()
                serializer.save()
            return Response({'response_code': status.HTTP_200_OK,
                             'message': "signed in succesfully",
                             'status_flag': True,
                             'status': "success",
                             'error_details': None,
                             'data': serializer.data})
        except Exception as error:
            return Response({'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': "cant register",
                             'status_flag': False,
                             'status': "Failed",
                             'error_details': str(error),
                             'data': []})


class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'])
            if user:
                pas = hashlib.sha256(bytes.fromhex(user.salt)+request.data['password'].encode('utf-8')).hexdigest()  # Encode the password
                if pas == user.password:
                    serializer = RegisterSerializer(instance=user)
                    return Response({'response_code': status.HTTP_200_OK,
                                     'message': "signed in successfully",
                                     'status_flag': True,
                                     'status': "success",
                                     'error_details': None,
                                     'data': serializer.data})
                return Response("wrong credentials")
                #{"db_pass": password,'pas':request.data['password'].encode('utf-8'), 'user_pas': pas, 'salt': user.salt, 'data': 'wrong credential'}
            return Response('user not registered')

        except Exception as e:
            return Response({'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': "can't register",
                             'status_flag': False,
                             'status': "Failed",
                             'error_details': str(e),
                             'data': []})
