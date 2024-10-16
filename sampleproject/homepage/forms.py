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
            "email",
            "age",
            "salary",
            "designation",
            "password",
            "status",
            'img_description',
        ]
    def __init__(self, *args, **kwargs):
        super(GeeksForm, self).__init__(*args, **kwargs)
        self.fields['designation'].queryset = Group.objects.all()

class TOTPVerifyForm(forms.Form):
    token = forms.CharField(max_length=6, required=True, label="TOTP Token")