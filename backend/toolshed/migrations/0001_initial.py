# Generated by Django 4.2.2 on 2023-06-22 02:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('origin', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='toolshed.category')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('origin', models.CharField(max_length=255)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='toolshed.category')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit_symbol', models.CharField(blank=True, max_length=16, null=True)),
                ('unit_name', models.CharField(blank=True, max_length=255, null=True)),
                ('unit_name_plural', models.CharField(blank=True, max_length=255, null=True)),
                ('base2_prefix', models.BooleanField(default=False)),
                ('dimensions', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('origin', models.CharField(max_length=255)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='toolshed.category')),
            ],
            options={
                'verbose_name_plural': 'properties',
            },
        ),
    ]