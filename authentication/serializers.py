from rest_framework import serializers
from authentication.models import User, UserProfile
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

class UserProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'DOB','image']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,  min_length=6, write_only=True)
    class Meta:
        model=User
        fields = ['email', 'username', 'password']
    
    def validate(self, attrs):
        username = attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError('Username should contain alphanumeric values only')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model=User
        fields=['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model=User
        fields=['email','password','username']

    def validate(self, attrs):
        email= attrs.get('email','')
        password = attrs.get('password','')
        try:
            user = authenticate(email=email, password=password)
            if user is None:
                raise AuthenticationFailed("Invalid credentials given!!!")
            if not user.is_active:
                raise AuthenticationFailed("Account is deactivated!!!")
            if not user.is_verified:
                raise AuthenticationFailed("Email is not verified!!!")

        except serializers.ValidationError:
            return {'error':"Please provide email and password"}
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)

    class Meta:
        model = User
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email','')        
        try:
            user = User.objects.get(email=email)
            if not user.is_verified:
                raise serializers.ValidationError("This email id is not verified!!")
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not registerd")    
        return attrs


class NewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6)
    password2 = serializers.CharField(max_length=68, min_length=6)
        
    class Meta:
        model=User
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password','')
        password2 = attrs.get('password2','')        
        if password != password2:
            raise serializers.ValidationError("Password not matched!!")
        return attrs



