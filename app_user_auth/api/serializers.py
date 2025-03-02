from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
        read_only_fields = ['id']


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    display_name = serializers.CharField(required=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'repeated_password', 'display_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):

        if 'username' not in data:

            data['username'] = data['display_name'].replace(' ', '_').lower()

            base_username = data['username']
            counter = 1
            while User.objects.filter(username=data['username']).exists():
                data['username'] = f"{base_username}{counter}"
                counter += 1

        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email address is already in use.")
        return value

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        display_name = self.validated_data.get('display_name', '')

        if pw != repeated_pw:
            raise serializers.ValidationError({
                'password': 'Passwords must match.'
            })

        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'])

        account.set_password(pw)
        account.save()

        account.profile.display_name = display_name
        account.profile.save()

        return account


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

            if not user.check_password(password):
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
