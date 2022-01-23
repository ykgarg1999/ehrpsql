from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Profile

from django.contrib.auth import get_user_model
User = get_user_model()

# ProfileSerializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'speciality', 'id', 'gender']


# userInfoSerializer
class GetUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

    def get_profile(self, obj):
        try:
            profile = obj.profile
            return ProfileSerializer(profile).data
        except:
            return None

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("username or password Incorrect")

        return attrs




    # Register Serializer


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    gender = serializers.CharField(required=True)
    speciality = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'gender', 'speciality']
        write_only_fields = ['password']

    def validate(self, data):
        print(data)
        users_qs = User.objects.filter(email=data['email'])
        if users_qs.exists():
            raise serializers.ValidationError('user with this email already exists')
        else:
            return data

    def create(self, data):
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        user.set_password(data['password'])
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


# userVerificationSerializer
class UserValidationSer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data["username"])
        if user.exists():
            raise serializers.ValidationError({"username": "user with this username already exists"})

        user = User.objects.filter(email=data["email"])
        if user.exists():
            raise serializers.ValidationError({"email": "user with this email already exists"})

        return data
