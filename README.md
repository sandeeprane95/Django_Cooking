## The Recipe Book - A Django Rest Framework Project

In this project, I have created API endpoints using the Django Rest Framework. This project can allow a person to create and manage recipes as well as the authors/users of those recipes. It supplies the following REST API endpoints:  

1. Create User  
2. Create Recipe  
3. Get all recipes for a user  
4. List all the recipes  
5. Update a recipe  
6. Delete a recipe  



### Project Setup -  

Prerequisites - Python 3.7

1. Create a new virtual environment  
```
> virtualenv temp
```
2. Activate the virtual environment  
```
> source temp/bin/activate
```
3. Download and navigate to the Django Project Folder  
4. Install all the libraries/packages in the virtual environment  
```
> pip install -r requirements.txt
```
5. Go to Django_Cooking Folder  
6. Start the Django server on your localhost  
```
> python manage.py runserver
```
7. You can log in to the django admin using your browser  
```
> http://localhost:8000/admin/  
> username = admin, password = admin  
> Alternatively, you can create a new superuser using 'python manage.py createsuperuser'  
```



### API Implementation Details - 

The following are the permissible API calls:  

1. Create user [Type: POST]  
This API endpoint can be used to create the users/authors for the recipes.  
```
> http://localhost:8000/api/cook_book/user/create/  
> Supply the following content in the body of the call:  
{  
	"username" : string,     
	"first_name": string,  
	"last_name": string,  
	"email": string,  
	"password": string,  
}  
```     
2. Create Recipe [Type: POST]  
This API endpoint can be used to create the recipes.  
```
> http://localhost:8000/api/cook_book/user/create/  
> Supply the following content in the body of the call:  
{    
	"name" : string,                         //recipe name  
	"user": string,				 //recipe user's username   	
	"steps": [string_1, string_2, ...],      //recipe steps  
	"ingredients": [string1, string2, ...]   //recipe ingredients  
}  
```  
3. Get all recipes for a user [Type: GET]  
This API endpoint can be used to get all the recipes for a particular user. Further you can also specify   additional parameters like limit and offset to limit the number of entries that you see.  
```  
> http://localhost:8000/api/cook_book/user/get/    
> Supply the following content in the body of the call:    
{  
	"user": string,				 //recipe user's username  
}  
> Additional parameters: http://localhost:8000/api/cook_book/user/get/?limit=5&offset=0  
```  
4. List all the recipes [TYPE: GET]  
This API endpoint gives all the recipe instances. This also supports limit and offset params.  
```  
> http://localhost:8000/api/cook_book/user/list/  
> Additional parameters: http://localhost:8000/api/cook_book/user/list/?limit=5&offset=0  
```  
5. Update a recipe [TYPE: PUT]  
This API endpoint can be used to update a specific recipe instance.  
```  
> http://localhost:8000/api/cook_book/user/update/  
> Supply the following content in the body of the call:    
{  
	"name" : string,                         //recipe name (optional)  
	"user": string,				 //recipe user's username (optional)   	
	"steps": [  
		{"id": int, "step_text": string},  
		{"id": int, "step_text": string},  
		...],       		         //recipe steps (optional)  
	"ingredients": [  
		{"id": int, "text": string},  
		{"id": int, "text": string},  
		...],                            //recipe ingredients (optional)  
}  
```  
6. Delete a recipe [TYPE: DELETE]  
This API endpoint can be used to delete a specific recipe instance.  
```  
> http://localhost:8000/api/cook_book/user/delete/    
> Supply the following content in the body of the call:  
{  
	"id": string,				 //recipe id  
}   
```
