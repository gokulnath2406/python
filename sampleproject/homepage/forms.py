from django import forms
from .models import ElixirModel
from django_otp.forms import OTPAuthenticationForm



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

class TOTPVerifyForm(forms.Form):
    token = forms.CharField(max_length=6, required=True, label="TOTP Token")