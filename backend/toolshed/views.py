from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Profile, InventoryItem


@login_required(login_url="/login/")
def index(request):
    return render(request, 'pages/index.html')


@login_required(login_url="/login/")
def settings(request):
    return render(request, 'pages/settings.html')


@login_required(login_url="/login/")
def profile(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get_or_create(user=user)
    return render(request, 'pages/profile.html', {'user': user, 'profile': user_profile})


@login_required(login_url="/login/")
def inventory(request):
    return render(request, 'pages/inventory.html', {'items': InventoryItem.objects.all()})
