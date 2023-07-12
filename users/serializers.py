from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate


class RegisterUserSerializer(serializers.ModelSerializer):
    """ User register Serializer class """
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwags = {
            'email' : {
                'required' : True,
                'allow_blank': False
            },
            'first_name' : {
                'required' : False,
                'allow_blank': True
            },
            'last_name' : {
                'required' : False,
                'allow_blank': True
            },
            'password': {
                'write_only': True,
            }
        }
        
    
    def create(self, validated_data):
        """ Creation of new user """
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        
        user = User.objects.create(
            username = username,
            email = email,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
        
        return user
        

class LoginSerializer(serializers.Serializer):
    '''serializer for the user authentication object'''
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        
        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return user      