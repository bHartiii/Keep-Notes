from rest_framework import serializers
from authentication.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,  min_length=6, write_only=True, style={'input_type': 'password'})

    class Meta:
        model=User
        fields = ['email', 'username', 'password']
    
    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError('Username should contain alphanumeric values only')
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model=User
        fields=['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, style={'input_type': 'password'})
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model=User
        fields=['email','password','username']

    def validate(self, attrs):
        email= attrs.get('email','')
        password = attrs.get('password','')
        try:
            user = User.objects.get(email =email, password=password)
            if not user:
                raise AuthenticationFailed("Invalid credentials given!!!")
            if not user.is_active:
                raise AuthenticationFailed("Account is deactivated!!!")
            if not user.is_verified:
                raise AuthenticationFailed("Email is not verified!!!")

        except serializers.ValidationError as identifier:
            return {'error':"Please provide email and password"}

        return {
            'email':user.email,
            'username':user.username,
            'password':user.password,
        }

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

