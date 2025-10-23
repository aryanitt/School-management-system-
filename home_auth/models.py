from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone


# Custom User Model
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_authorized = models.BooleanField(default=False)

    # Custom roles
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    # Fix: related_name must be a string or None (not True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True
    )

    def __str__(self):
        return self.username


# Password Reset Model
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.CharField(
        max_length=32,
        default=get_random_string(32),
        editable=False,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Token validity period (e.g., 1 hour)
    TOKEN_VALIDITY_PERIOD = timezone.timedelta(hours=1)

    def is_valid(self):
        """Check if the token is still valid."""
        return timezone.now() <= self.created_at + self.TOKEN_VALIDITY_PERIOD

    def send_reset_email(self):
        """Send the reset link via email."""
        reset_link = f"http://localhost:8000/reset-password/{self.token}/"
        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password:\n{reset_link}\n\nNote: This link will expire in 1 hour.",
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return f"Password Reset Token for {self.user.username}"
