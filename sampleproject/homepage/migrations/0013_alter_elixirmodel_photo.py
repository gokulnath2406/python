# Generated by Django 5.1 on 2024-10-14 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0012_rename_description_elixirmodel_img_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elixirmodel',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
