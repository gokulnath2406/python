# Generated by Django 5.1 on 2024-09-27 06:24

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_elixirmodel_email_elixirmodel_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elixirmodel',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='', max_length=128, region='IN'),
        ),
    ]
