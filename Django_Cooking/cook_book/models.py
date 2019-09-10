from django.db import models
from django.contrib.auth.models import User

# Recipe Model - Recipes belong to specific users
class Recipe(models.Model):
	name = models.CharField(max_length = 255, null = False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name


# Step Model - Steps for a recipe.
class Step(models.Model):
	step_text = models.TextField(null = False)
	recipe = models.ForeignKey(Recipe, related_name = 'recipe_step',
		on_delete=models.CASCADE)

	def __str__(self):
		return self.step_text[:255]

# Ingredient Model - Ingredients for a recipe
class Ingredient(models.Model):
	text = models.CharField(max_length = 255, null = False)
	recipe = models.ForeignKey(Recipe, related_name = 'recipe_ingredient', 
		on_delete=models.CASCADE)

	def __str__(self):
		return self.text