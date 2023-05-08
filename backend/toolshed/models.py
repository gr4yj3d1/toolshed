from django.db import models
from django_softdelete.models import SoftDeleteModel

from authentication.models import ToolshedUser, KnownIdentity


class InventoryItem(SoftDeleteModel):
    published = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    availability_policy = models.CharField(max_length=255)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_items')
    owned_amount = models.IntegerField()
    owner = models.ForeignKey(ToolshedUser, on_delete=models.CASCADE, related_name='inventory_items')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ItemProperty(models.Model):
    value = models.CharField(max_length=255)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='item_properties')
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='properties')

    def __str__(self):
        return self.name


class ItemTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='item_tags')
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name


class LendingPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='lending_periods')

    def __str__(self):
        return self.name


#class Event(models.Model):
#    name = models.CharField(max_length=255)
#    description = models.TextField()
#    location = models.CharField(max_length=255)
#    date = models.DateField()
#    time = models.TimeField()
#    # host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
#    host_username = models.CharField(max_length=255)
#    host_domain = models.CharField(max_length=255)
#
#    def __str__(self):
#        return self.name


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    item_requested = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='requested_transactions')
    item_offered = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='offered_transactions')
    requester = models.ForeignKey(ToolshedUser, on_delete=models.CASCADE, related_name='requested_transactions')
    offerer = models.ForeignKey(ToolshedUser, on_delete=models.CASCADE, related_name='offered_transactions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requester} requests {self.item_requested} from {self.offerer} in exchange for {self.item_offered}"


class Message(models.Model):
    sender = models.ForeignKey(ToolshedUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(ToolshedUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient} at {self.created_at}"


class Profile(models.Model):
    user = models.OneToOneField(ToolshedUser, on_delete=models.CASCADE)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
