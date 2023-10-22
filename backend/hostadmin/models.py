from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey('authentication.ToolshedUser', on_delete=models.CASCADE, related_name='domains')
    open_registration = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ImportedIdentifierSets(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
