from django.db import models
from django.contrib.auth.models import User, Group
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import EmailValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class MaritalStatus(models.Model):
    STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, unique=True)
    
    def __str__(self):
        return self.status

class DateOfBirth(models.Model):
    date_of_birth = models.DateField()
    
    def __str__(self):
        return self.date_of_birth.strftime('%Y-%m-%d')

class ElixirModel(models.Model):
    photo = models.ImageField(upload_to='media/', null=True, blank=True)
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = PhoneNumberField(max_length=128, default="", region='IN')
    email = models.EmailField(blank=True, default="@elixir.com")
    personal_email = models.EmailField(blank=True, default="")
    designation = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    salary = models.IntegerField()
    password = models.CharField(max_length=15)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

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

class Attendance(models.Model):
    employee = models.ForeignKey(ElixirModel, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')])
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')  # Ensure unique attendance records per employee per day

    def __str__(self):
        return f"{self.employee.username} - {self.date}"
