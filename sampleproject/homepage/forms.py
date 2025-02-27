from django import forms
from .models import ElixirModel
from django_otp.forms import OTPAuthenticationForm
from django.contrib.auth.models import User, Group



# creating a form
class GeeksForm(forms.ModelForm):

    # create meta class
    class Meta:
        # specify model to be used
        model = ElixirModel

        # specify fields to be used
        fields = [
            'photo',
            "name",
            "phone_number",
            "personal_email",
            "email",
            "date_of_birth",
            'marital_status',
            "salary",
            "designation",
            "password",
            "status",
        ]
    def __init__(self, *args, **kwargs):
        super(GeeksForm, self).__init__(*args, **kwargs)
        self.fields['designation'].queryset = Group.objects.all()

class TOTPVerifyForm(forms.Form):
    token = forms.CharField(max_length=6, required=True, label="TOTP Token")