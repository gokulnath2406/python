# import the standard Django Model
# from built-in library
from django.db import models

# declare a new model with a name "GeeksModel"
class ElixirModel(models.Model):

	# fields of the model
	name = models.CharField(max_length = 200)
	designation = models.CharField(max_length = 200)
	status = models.BooleanField(default = True)
	age = models.IntegerField()
	salary = models.IntegerField()

	def __str__(self):
		return self.name