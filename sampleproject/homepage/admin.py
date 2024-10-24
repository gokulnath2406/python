from django.contrib import admin
from django.contrib.auth.models import User
from .models import ElixirModel, MaritalStatus, DateOfBirth, Attendance

class ElixirModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'designation', 'status', 'salary', 'get_date_of_birth', 'marital_status')
    search_fields = ('name', 'email', 'designation')

    def get_date_of_birth(self, obj):
        return obj.date_of_birth.date_of_birth if obj.date_of_birth else None
    get_date_of_birth.short_description = 'Date of Birth'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Create User on new ElixirModel creation
            username = obj.name
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{obj.name}{counter}"
                counter += 1
            user = User.objects.create_user(username=username, password=obj.password, email=obj.email)
            obj.user = user
            obj.save()
        else:  # Update User on ElixirModel update
            user = obj.user
            user.username = obj.name
            user.set_password(obj.password)
            user.email = obj.email
            user.save()

admin.site.register(ElixirModel, ElixirModelAdmin)
admin.site.register(MaritalStatus)
admin.site.register(DateOfBirth)
admin.site.register(Attendance)
