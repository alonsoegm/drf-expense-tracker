"""
Authentication Views

What are we creating?
- RegisterView: User registration
- LoginView: User login (get JWT tokens)
- LogoutView: Blacklist refresh token
- CurrentUserView: Get/Update current user
- ChangePasswordView: Change password

Compare to C#:
[ApiController]
[Route("api/auth")]
public class AuthController : ControllerBase {
    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterDto dto) { }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginDto dto) { }
}
"""

# Standard Library
from textwrap import dedent

# Third-party
from django.contrib.auth.models import User
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    ChangePasswordSerializer,
    RegisterSerializer,
    UpdateUserSerializer,
    UserSerializer,
)


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint

    POST /api/auth/register/
    {
        "username": "john",
        "email": "john@example.com",
        "password": "SecurePass123!",
        "password2": "SecurePass123!",
        "firstName": "John",
        "lastName": "Doe"
    }

    Response:
    {
        "user": {
            "id": 1,
            "username": "john",
            "email": "john@example.com",
            "firstName": "John",
            "lastName": "Doe"
        },
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }

    Compare to C#:
    [HttpPost("register")]
    [AllowAnonymous]
    public async Task<IActionResult> Register([FromBody] RegisterDto dto) {
        var user = new User { UserName = dto.Username, Email = dto.Email };
        var result = await _userManager.CreateAsync(user, dto.Password);

        if (result.Succeeded) {
            var token = _tokenService.GenerateToken(user);
            return Ok(new { user, token });
        }
        return BadRequest(result.Errors);
    }
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Anyone can register
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="Register a new user",
        description=dedent(
            """
            Create a new user account and receive JWT tokens immediately.

            **No authentication required** for this endpoint.

            **Password requirements:**
            - At least 8 characters
            - Cannot be too common
            - Cannot be entirely numeric

            **Returns:**
            - User information
            - Access token (valid for 60 minutes)
            - Refresh token (valid for 7 days)
        """
        ).strip(),
        examples=[
            OpenApiExample(
                "Register Example",
                value={
                    "username": "johndoe",
                    "email": "john@example.com",
                    "password": "SecurePass123!",
                    "passwordConfirm": "SecurePass123!",
                    "firstName": "John",
                    "lastName": "Doe",
                },
                request_only=True,
            ),
        ],
        tags=["Authentication"],
    )
    def create(self, request, *args, **kwargs):
        """
        Create user and return JWT tokens
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create user
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Return user data + tokens
        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """
    User login endpoint

    Uses djangorestframework-simplejwt's TokenObtainPairView

    POST /api/auth/login/
    {
        "username": "john",
        "password": "SecurePass123!"
    }

    Response:
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }

    Compare to C#:
    [HttpPost("login")]
    [AllowAnonymous]
    public async Task<IActionResult> Login([FromBody] LoginDto dto) {
        var user = await _userManager.FindByNameAsync(dto.Username);

        if (user != null && await _userManager.CheckPasswordAsync(user, dto.Password)) {
            var token = _tokenService.GenerateToken(user);
            return Ok(new { token });
        }

        return Unauthorized();
    }
    """

    permission_classes = (AllowAny,)  # type: ignore[assignment]

    @extend_schema(
        summary="Login to get JWT tokens",
        description=dedent(
            """
        Authenticate with username and password to receive JWT tokens.

        **No authentication required** for this endpoint.

        **Returns:**
        - Access token (valid for 60 minutes)
        - Refresh token (valid for 7 days)

        **Usage:**
        1. Login to get tokens
        2. Use access token in Authorization header: `Bearer <token>`
        3. When access token expires, use refresh token to get new access token
    """
        ).strip(),
        examples=[
            OpenApiExample(
                "Login Example",
                value={"username": "johndoe", "password": "SecurePass123!"},
                request_only=True,
            ),
        ],
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    """
    Logout endpoint (blacklist refresh token)

    POST /api/auth/logout/
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }

    Response:
    {
        "detail": "Successfully logged out."
    }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Add to blacklist

            return Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """
    Get or update current user

    GET /api/auth/me/
    Response:
    {
        "id": 1,
        "username": "john",
        "email": "john@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "dateJoined": "2024-03-19T..."
    }

    PATCH /api/auth/me/
    {
        "firstName": "Jonathan",
        "email": "newemail@example.com"
    }

    Compare to C#:
    [HttpGet("me")]
    [Authorize]
    public IActionResult GetCurrentUser() {
        var user = await _userManager.GetUserAsync(User);
        return Ok(_mapper.Map<UserDto>(user));
    }

    [HttpPatch("me")]
    [Authorize]
    public async Task<IActionResult> UpdateProfile([FromBody] UpdateUserDto dto) {
        var user = await _userManager.GetUserAsync(User);
        user.FirstName = dto.FirstName;
        user.Email = dto.Email;
        await _userManager.UpdateAsync(user);
        return Ok(_mapper.Map<UserDto>(user));
    }
    """

    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return the current authenticated user"""
        return self.request.user

    def get_serializer_class(self):
        """Use different serializers for GET vs PATCH"""
        if self.request.method == "GET":
            return UserSerializer
        return UpdateUserSerializer

    @extend_schema(
        summary="Get current user information",
        description=dedent(
            """
            Get information about the currently authenticated user.

            **Requires authentication.**
        """
        ).strip(),
        tags=["Authentication"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update current user profile",
        description=dedent(
            """
            Update the current user's profile information.

            **Requires authentication.**

            Only firstName, lastName, and email can be updated.
            Username cannot be changed.
        """
        ).strip(),
        examples=[
            OpenApiExample(
                "Update Profile",
                value={"firstName": "Jonathan", "email": "newemail@example.com"},
                request_only=True,
            ),
        ],
        tags=["Authentication"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ChangePasswordView(generics.UpdateAPIView):
    """
    Change password endpoint

    POST /api/auth/change-password/
    {
        "oldPassword": "OldPass123!",
        "newPassword": "NewPass123!",
        "newPassword2": "NewPass123!"
    }

    Response:
    {
        "detail": "Password updated successfully."
    }

    Compare to C#:
    [HttpPost("change-password")]
    [Authorize]
    public async Task<IActionResult> ChangePassword([FromBody] ChangePasswordDto dto) {
        var user = await _userManager.GetUserAsync(User);
        var result = await _userManager.ChangePasswordAsync(
            user, dto.OldPassword, dto.NewPassword);

        if (result.Succeeded) {
            return Ok(new { message = "Password changed successfully" });
        }
        return BadRequest(result.Errors);
    }
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        """Return the current authenticated user"""
        return self.request.user

    @extend_schema(
        summary="Change password",
        description=dedent(
            """
            Change the current user's password.

            **Requires authentication.**

            After changing password, you'll need to login again to get new tokens.
        """
        ).strip(),
        examples=[
            OpenApiExample(
                "Change Password",
                value={
                    "oldPassword": "OldPass123!",
                    "newPassword": "NewSecurePass123!",
                    "newPasswordConfirm": "NewSecurePass123!",
                },
                request_only=True,
            ),
        ],
        tags=["Authentication"],
    )
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
        )
