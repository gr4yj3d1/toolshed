from django.contrib.auth.models import User
from django.db import models


class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    #owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tools')
    owner_username = models.CharField(max_length=255)
    owner_domain = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    #host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    host_username = models.CharField(max_length=255)
    host_domain = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    tool_requested = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='requested_transactions')
    tool_offered = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='offered_transactions')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_transactions')
    offerer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offered_transactions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requester} requests {self.tool_requested} from {self.offerer} in exchange for {self.tool_offered}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
