# Generated by Django 5.1 on 2024-10-24 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0022_elixirmodel_personal_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elixirmodel',
            name='personal_email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]
