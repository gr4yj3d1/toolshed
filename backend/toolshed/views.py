import itertools

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from .aggregators import timeline_notifications, unread_messages
from .models import Profile, InventoryItem


@login_required(login_url="/login/")
def index(request):
    user = request.user
    notifications = itertools.islice(timeline_notifications(request.user), 5)
    messages = itertools.islice(unread_messages(request.user), 5)
    return render(request, 'pages/index.html',
                  {'top_notifications': notifications, 'top_messages': messages, 'user': request.user})


@login_required(login_url="/login/")
def settings(request):
    user = request.user
    notifications = itertools.islice(timeline_notifications(request.user), 5)
    messages = itertools.islice(unread_messages(request.user), 5)
    return render(request, 'pages/settings.html',
                  {'top_notifications': notifications, 'top_messages': messages, 'user': request.user})


@login_required(login_url="/login/")
def profile(request, username):
    user = request.user
    notifications = itertools.islice(timeline_notifications(request.user), 5)
    messages = itertools.islice(unread_messages(request.user), 5)
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get_or_create(user=user)
    return render(request, 'pages/profile.html',
                  {'top_notifications': notifications, 'top_messages': messages, 'user': request.user,
                   'profile': user_profile})


@login_required(login_url="/login/")
def inventory(request):
    user = request.user
    notifications = itertools.islice(timeline_notifications(request.user), 5)
    messages = itertools.islice(unread_messages(request.user), 5)
    return render(request, 'pages/inventory.html',
                  {'top_notifications': notifications, 'top_messages': messages, 'user': request.user,
                   'items': InventoryItem.objects.all()})
