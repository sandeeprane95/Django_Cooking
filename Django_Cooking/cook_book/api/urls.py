from django.conf.urls import url
from .views import (
	UserCreateAPIView,
    RecipeCreateAPIView,
    RecipeRetrieveAPIView,
    RecipeListAPIView,
    RecipeDeleteAPIView,
    RecipeUpdateAPIView,
	)


# Includes all API url patterns
urlpatterns = [
    url(r'^user/create/?', UserCreateAPIView.as_view(), 
    	name='user_create'),
    url(r'^recipe/create/?', RecipeCreateAPIView.as_view(),
        name='recipe_create'),
    url(r'^recipe/get/?', RecipeRetrieveAPIView.as_view(),
        name='recipe_get'),
    url(r'^recipe/list/?', RecipeListAPIView.as_view(),
        name='recipe_list'),
    url(r'^recipe/delete/?', RecipeDeleteAPIView.as_view(),
        name='recipe_delete'),
    url(r'^recipe/update/?', RecipeUpdateAPIView.as_view(),
        name='recipe_update'),    
]