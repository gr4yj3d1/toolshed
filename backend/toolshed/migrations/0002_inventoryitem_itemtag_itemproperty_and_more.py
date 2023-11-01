# Generated by Django 4.2.2 on 2023-06-22 02:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('toolshed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('published', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('availability_policy', models.CharField(max_length=255)),
                ('owned_quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory_items', to='toolshed.category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toolshed.inventoryitem')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toolshed.tag')),
            ],
        ),
        migrations.CreateModel(
            name='ItemProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('inventory_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toolshed.inventoryitem')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toolshed.property')),
            ],
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='properties',
            field=models.ManyToManyField(through='toolshed.ItemProperty', to='toolshed.property'),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='tags',
            field=models.ManyToManyField(related_name='inventory_items', through='toolshed.ItemTag', to='toolshed.tag'),
        ),
    ]