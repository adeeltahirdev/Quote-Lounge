from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from .models import Profile
from quotes.models import Quote

User = get_user_model()  # ✅ fixed

# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm-password', '')

        if password != confirm_password:
            messages.info(request, 'Password does not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already registered')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')

    return render(request, 'auth/register.html')


# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid credentials!')
            return redirect('login')

    return render(request, 'auth/login.html')


# Logout view
def logout(request):
    auth.logout(request)
    return redirect('index')


def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You need to login first.')
        return redirect('login')

    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        bio = request.POST.get('bio','')
        profile_picture = request.POST.get('profile_picture')
        
        profile.bio = bio 
        if profile_picture:
            profile.profile_picture = profile_picture
        
        profile.save()
        messages.info(request, 'Profile updated!')
        return redirect('profile')
    
    
    quotes = Quote.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'quotes': quotes,
    }
    return render(request, 'auth/profile.html', context)