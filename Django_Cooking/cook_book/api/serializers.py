from rest_framework import serializers
from cook_book.models import (
	Step,
	Ingredient,
	Recipe
	)
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


# Serializer used to create a new user record
class UserCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'first_name',
			'last_name',
			'password',
		]

	def validate(self, data):
		if not data.get('username') or not data.get('email'):
			raise serializers.ValidationError("The fields cannot be " 
				"blank.")
		
		if not data.get('password'):
			raise serializers.ValidationError("The password field cannot be"
			" blank.")		
		
		return data 

	def create(self, validated_data):
		password = validated_data.pop('password')
		instance = self.Meta.model(**validated_data)
		instance.set_password(password)
		instance.save()
		
		return instance


# Serializer used for Recipe steps
class StepSerializer(serializers.ModelSerializer):
	class Meta:
		model = Step
		fields = ['id','step_text']


# Serializer used for Recipe ingredients
class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ingredient
		fields = ['id','text']


# Serializer used for creating a recipe
class RecipeCreateSerializer(serializers.ModelSerializer):
	steps = StepSerializer(many=True)
	ingredients = IngredientSerializer(many=True)

	class Meta:
		model = Recipe
		fields = [
			'id',
			'name',
			'user',
			'steps',
			'ingredients', 
		]

	def validate(self, data):
		if not data.get('name') or not data.get('steps') or \
		not data.get('ingredients'):
			raise serializers.ValidationError('The fields cannot be blank')
		
		return data

	def create(self, validated_data):
		steps_data = validated_data.pop('steps')
		ingredients_data = validated_data.pop('ingredients')
		recipe_instance = Recipe.objects.create(**validated_data)
		
		for a_step in steps_data:
			Step.objects.create(recipe=recipe_instance, 
				step_text=a_step['step_text'])
		
		for a_ingredient in ingredients_data:
			Ingredient.objects.create(recipe=recipe_instance, 
				text=a_ingredient['text'])
		
		return recipe_instance


# Serializer used for retrieving a recipe by user
class RecipeRetrieveSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source='user.username')
	steps = serializers.SerializerMethodField()
	ingredients = serializers.SerializerMethodField()

	class Meta:
		model = Recipe
		fields = [
			'id',
			'user',
			'name',
			'steps',
			'ingredients',
		]

	def get_steps(self, obj):
		return (StepSerializer(obj.recipe_step.all(), many=True).data)

	def get_ingredients(self, obj):
		return (IngredientSerializer(obj.recipe_ingredient.all(), 
			many=True).data)


# Serializer used for deleting a recipe instance
class RecipeDeleteSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()

	class Meta:
		model = Recipe
		fields = [
			'id'
		]

	def perform_destroy(self, instance):
		instance.delete()