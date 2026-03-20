"""
Authentication Serializers

What are we creating?
- UserSerializer: User data representation
- RegisterSerializer: User registration
- LoginSerializer: User login
- ChangePasswordSerializer: Password change

Compare to C#:
public class RegisterDto {
    public string Username { get; set; }
    public string Email { get; set; }
    public string Password { get; set; }
}
"""

# Third-party
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    """
    User data serializer

    Used for:
    - GET /api/auth/me/ (current user info)
    - Response after registration

    Compare to C#:
    public class UserDto {
        public int Id { get; set; }
        public string Username { get; set; }
        public string Email { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
    }
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    User registration serializer

    IMPORTANT: Using password_confirm instead of password2
    to avoid camelCase conversion issues with djangorestframework-camel-case
    """

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    # Changed from password2 to password_confirm
    password_confirm = serializers.CharField(
        write_only=True, required=True, help_text="Confirm password"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate(self, attrs):
        """
        Object-level validation

        Check that password and password_confirm match
        """
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """
        Create new user

        Remove password_confirm (not a model field)
        Use create_user() to hash password
        """
        # Remove password_confirm (not needed for user creation)
        validated_data.pop("password_confirm")

        # Create user with hashed password
        user = User.objects.create_user(**validated_data)

        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Change password serializer
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    # Changed from new_password2 to new_password_confirm
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        """Validate that new passwords match"""
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        """Validate that old password is correct"""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Update user profile serializer

    PATCH /api/auth/me/
    {
        "firstName": "John",
        "lastName": "Doe",
        "email": "newemail@example.com"
    }
    """

    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

    def validate_email(self, value):
        """Validate email is unique (excluding current user)"""
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
