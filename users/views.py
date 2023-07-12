from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterUserSerializer, LoginSerializer
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView



class LoginView(KnoxLoginView):
    """ This is the login """
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        # _, token = AuthToken.objects.create(user)

        return super(LoginView, self).post(request, format=None)
        # return Response({
        #     'user_informations' : {
        #         'id': user.id,
        #         'username': user.username,
        #         'email': user.email
        #     },
        #     'token': token
        # })



class RegisterView(APIView):
    """ This is the register view, it creates a new user and return his informations with token """
    
    def post(self, request, format=None):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        
        return Response({
            'user_informations' : {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'token': token
        })
        
