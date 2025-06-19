from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.

    Provides basic user information for use in other serializers
    and API responses.
    """

    class Meta:
        model = User
        fields = ["id", "username"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles new user creation with email validation and password requirements.

    Attributes:
        email: User's email with uniqueness validation
        password: User's password (write-only field)
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data: dict) -> User:
        """
        Create and return a new user instance.

        Args:
            validated_data (dict): Dictionary containing 'username', 'email',
                                 and 'password' fields.

        Returns:
            User: Newly created user instance.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user
