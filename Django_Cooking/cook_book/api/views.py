from .serializers import (
	UserCreateSerializer,
	RecipeCreateSerializer,
	RecipeRetrieveSerializer,
	RecipeDeleteSerializer,
	)
from cook_book.models import (
	Step,
	Ingredient,
	Recipe
	)
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.pagination import LimitOffsetPagination



# View for creating a user
class UserCreateAPIView(APIView):
	serializer_class = UserCreateSerializer

	def post(self, request, *args, **kwargs):
		data = request.data
		
		serializer = UserCreateSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response({'message': 'A new user record has been '
				'created'}, status=HTTP_200_OK)
		
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



# View for creating a recipe
class RecipeCreateAPIView(APIView):
	serializer_class = RecipeCreateSerializer

	def post(self, request, *args, **kwargs):
		data = request.data.copy()
		
		try:
			user_obj = User.objects.get(username=data['user'])
		except:
			return Response({'message': 'The user does not exist'}, 
				status=HTTP_400_BAD_REQUEST)
		
		data['user'] = user_obj.id
		steps = data.get('steps', None)	
		
		# Create step list for Step model
		new_steps = []
		for a_step in steps:
			new_steps.append({'step_text' : a_step})
		data['steps'] = new_steps

		# Create ingredient list for Ingredient model
		ingredients = data.get('ingredients', None)	
		new_ingredients = []
		for a_ingredient in ingredients:
			new_ingredients.append({'text' : a_ingredient})
		data['ingredients'] = new_ingredients

		serializer = RecipeCreateSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response({'message': 'A new recipe has been '
				'created'}, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



# View for retrieving recipes by username
class RecipeRetrieveAPIView(APIView):
	serializer_class = RecipeRetrieveSerializer

	def get(self, request, *args, **kwargs):
		data = request.data
		paginator = LimitOffsetPagination()
		
		if 'user' not in data:
			return Response({'message': 'Please enter the user name'}, 
				status=HTTP_400_BAD_REQUEST)
		
		try:
			user_obj = User.objects.get(username=data['user'])
		except:
			return Response({'message' : 'The given user does not exist'},
				status=HTTP_400_BAD_REQUEST)
		
		queryset = Recipe.objects.filter(user=user_obj.id)
		
		if queryset.count()>0:
			context = paginator.paginate_queryset(queryset, request)
			serializer = RecipeRetrieveSerializer(context, many=True)
			return paginator.get_paginated_response(serializer.data)
		else:	
			return Response({'message': 'There are no recipes for the given '
				'user'}, status=HTTP_200_OK)	



# View for listing all the recipes
class RecipeListAPIView(APIView):
	serializer_class = RecipeRetrieveSerializer
	
	def get(self, request, *args, **kwargs):
		paginator = LimitOffsetPagination()
		data = request.data
		
		queryset = Recipe.objects.all()
		
		if queryset.count()>0:
			context = paginator.paginate_queryset(queryset, request)
			serializer = RecipeRetrieveSerializer(context, many=True)
			return paginator.get_paginated_response(serializer.data)
		else:	
			return Response({'message': 'There are no recipe records'}, 
				status=HTTP_200_OK)



# View for deleting a recipe
class RecipeDeleteAPIView(APIView):
	serializer_class = RecipeDeleteSerializer

	def delete(self, request, *args, **kwargs):
		data = request.data
		
		try:
			queryset = Recipe.objects.get(id = data['id'])
		except:
			return Response({'message': 'The given recipe ID is invalid'}, 
				status=HTTP_400_BAD_REQUEST)
		
		serializer = RecipeDeleteSerializer(queryset, data=data)
		serializer.perform_destroy(queryset)
		return Response({'message': 'The recipe with ID {} has been '
				'deleted'.format(data['id'])}, status=HTTP_200_OK)



# View for updating a recipe instance
class RecipeUpdateAPIView(APIView):
	def put(self, request, *args, **kwargs):
		data = request.data
		recipe_id = data.get('id', None)
		
		if recipe_id is None:
			return Response({'message': 'Recipe ID not provided'})	
		
		try:
			recipe_obj = Recipe.objects.get(id=data['id'])
		except:
			return Response({'message': 'The given recipe ID is invalid'})
		
		# Fetch current step and ingredient instances for the given recipe
		steps = recipe_obj.recipe_step.all()
		ingredients = recipe_obj.recipe_ingredient.all()
		
		# Check if recipe user is being updated 
		if data.get('user', None):
			try:
				user_obj = User.objects.get(username=data['user'])
			except:
				return Response({'message': 'The given user name is invalid'})
			recipe_obj.user = user_obj
		
		# Check if recipe name is being updated
		if data.get('name', None):
			recipe_obj.name = data['name']
		
		# Check if recipe steps are being updated
		if data.get('steps', None):
			if type(data['steps']) is not list:
				new_steps = []
				new_steps.append(data['steps'])
			else:
				new_steps = data['steps']
			for a_step in new_steps:
				if a_step.get('id', None):
					step = steps.filter(id=a_step['id'])[0] 
					step.step_text = a_step['step_text']
					step.save()
		
		# Check if recipe ingredients are being updated
		if data.get('ingredients', None):
			if type(data['ingredients']) is not list:
				new_ingredients = []
				new_ingredients.append(data['ingredients'])
			else:
				new_ingredients = data['ingredients']
			for a_ingredient in new_ingredients:
				if a_ingredient.get('id', None):
					ingredient = ingredients.filter(id=a_ingredient['id'])[0] 
					ingredient.text = a_ingredient['text']
					ingredient.save()
	
		recipe_obj.save()
		return Response({'message' : 'The recipe ID {} has been updated'\
			.format(data['id'])}, status=HTTP_200_OK)