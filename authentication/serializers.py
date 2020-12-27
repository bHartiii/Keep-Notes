from rest_framework import serializers
from authentication.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

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
    password = serializers.CharField(max_length=68, min_length=6, write_only=True, style={'input_type': 'password'})
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model=User
        fields=['email','password','username','tokens']

    def validate(self, attrs):
        email= attrs.get('email','')
        password = attrs.get('password','')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials given!!!")
        if not user.is_active:
            raise AuthenticationFailed("Account is deactivated!!!")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified!!!")
        return {
            'email':user.email,
            'username':user.username,
            'tokens': user.tokens()
        }

class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6)
    password2 = serializers.CharField(max_length=68, min_length=6,style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['email','password','password2']

    
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        password2 = attrs.get('password2','')
        
        try:
            user = User.objects.get(email=email)
            if password != password2:
                raise serializers.ValidationError("Password not matched!!")
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not registerd")
    
        return attrs

class NewPasswordSerializer(serializers.ModelSerializer):

    token = serializers.CharField(max_length=555)
        
    class Meta:
        model=User
        fields = ['token']