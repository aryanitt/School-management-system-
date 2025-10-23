from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.utils.crypto import get_random_string
from .models import CustomUser, PasswordResetRequest


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Create user
        user = CustomUser.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        # Assign role
        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True

        user.save()
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('index')

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid user role')
                return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials')

    return render(request, 'authentication/login.html')


def forget_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.create(
                user=user, email=email, token=token
            )

            # Print link in terminal for localhost
            reset_link = f"http://127.0.0.1:8000/authentication/reset-password/{token}"
            print(f"\n🔗 Password Reset Link: {reset_link}\n")

            reset_request.send_reset_email()  # Optional if you set up email
            messages.success(request, 'Reset link generated! Check your console (localhost).')
        else:
            messages.error(request, 'Email not found.')

    return render(request, 'authentication/forgot-password.html')


def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()

    if not reset_request or not reset_request.is_valid():
        messages.error(request, "Invalid or expired reset link.")
        return redirect('forget-password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user = reset_request.user
            user.set_password(new_password)
            user.save()
            reset_request.delete()
            messages.success(request, "Password reset successful! Please log in.")
            return redirect('login')

    return render(request, 'authentication/reset_password.html', {'token': token})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')
