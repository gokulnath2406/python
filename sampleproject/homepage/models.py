# import the standard Django Model
# from built-in library
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import EmailValidator
# declare a new model with a name "GeeksModel"
class ElixirModel(models.Model):

	# fields of the model
	name = models.CharField(max_length = 200)
	phone_number = PhoneNumberField(max_length=128, default="", region='IN')
	email = models.EmailField(blank=True, default="@elixir.com")
	designation = models.CharField(max_length = 200)
	status = models.BooleanField(default = True)
	age = models.IntegerField()
	salary = models.IntegerField()
	password = models.CharField(max_length = 15)

	def __str__(self):
		return self.name