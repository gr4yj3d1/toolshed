# Generated by Django 4.2.2 on 2023-07-07 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
        ('toolshed', '0002_inventoryitem_itemtag_itemproperty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='files',
            field=models.ManyToManyField(related_name='connected_items', to='files.file'),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='availability_policy',
            field=models.CharField(default='private', max_length=255),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]