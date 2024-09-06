from django import forms
from .models import ElixirModel


# creating a form
class GeeksForm(forms.ModelForm):

	# create meta class
	class Meta:
		# specify model to be used
		model = ElixirModel

		# specify fields to be used
		fields = [
			"name",
			"age",
			"status",
			"salary",
			"designation"
		]