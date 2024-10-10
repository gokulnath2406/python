from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import EmailValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class ElixirModel(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', default=1)
    phone_number = PhoneNumberField(max_length=128, default="", region='IN')
    email = models.EmailField(blank=True, default="@elixir.com")
    designation = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    age = models.IntegerField()
    salary = models.IntegerField()
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.name

@receiver(post_save, sender=ElixirModel)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        username = instance.name
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{instance.name}{counter}"
            counter += 1
        user = User.objects.create_user(username=username, password=instance.password, email=instance.email)
        instance.user = user
        instance.save()
    else:
        user = instance.user
        user.username = instance.name
        user.set_password(instance.password)
        user.email = instance.email
        user.save()

