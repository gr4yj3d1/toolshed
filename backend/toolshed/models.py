from django.db import models
from django.core.validators import MinValueValidator
from django_softdelete.models import SoftDeleteModel

from authentication.models import ToolshedUser, KnownIdentity


class Category(SoftDeleteModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    origin = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        parent = str(self.parent) + "/" if self.parent else ""
        return parent + self.name


class Property(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='properties')
    unit_symbol = models.CharField(max_length=16, null=True, blank=True)
    unit_name = models.CharField(max_length=255, null=True, blank=True)
    unit_name_plural = models.CharField(max_length=255, null=True, blank=True)
    base2_prefix = models.BooleanField(default=False)
    dimensions = models.IntegerField(null=False, blank=False, default=1, validators=[MinValueValidator(1)])
    origin = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'properties'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='tags')
    origin = models.CharField(max_length=255)

    def __str__(self):
        return self.name
