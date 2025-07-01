import requests
import json
import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages # Keep this if you plan to use Django messages
from datetime import datetime # Keep this if you use datetime objects




from .restapis import get_request, analyze_review_sentiments, post_request # Assuming you have these
from .populate import initiate
from .models import CarMake, CarModel, Dealer # Ensure all models are imported

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed
import json
from django.contrib.auth import authenticate, login
from .restapis import get_request, analyze_review_sentiments, post_review


logger = logging.getLogger(__name__) # Initialize logger once

# --- User Authentication Views ---

# @csrf_exempt
# def login_user(request):
#     data = json.loads(request.body)
#     username = data.get('userName')
#     password = data.get('password')
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         login(request, user)
#         data = {"userName": username, "status": "Authenticated"}
#     else:
#         data = {"userName": username, "status": "Failed to authenticate"} # More informative
#     return JsonResponse(data) 

# @csrf_exempt
# def login_user(request):
#     # Get username and password from request.POST dictionary
#     data = json.loads(request.body)
#     username = data['userName']
#     password = data['password']
#     # Try to check if provide credential can be authenticated
#     user = authenticate(username=username, password=password)
#     data = {"userName": username}
#     if user is not None:
#         # If user is valid, call login method to login current user
#         login(request, user)
#         data = {"userName": username, "status": "Authenticated"}
#     return JsonResponse(data)


@csrf_exempt # Consider removing or replacing with token-based authentication
def login_user(request):
    # 1. Check for POST request
    if request.method != 'POST':
        return JsonResponse({"status": "Invalid request method"}, status=405) # 405 Method Not Allowed

    try:
        # 2. Handle potential JSON decoding errors
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "Invalid JSON format"}, status=400) # 400 Bad Request

    username = data.get('userName')
    password = data.get('password')

    # Basic input validation
    if not username or not password:
        return JsonResponse({"status": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        # 3. Successful login response
        return JsonResponse({"userName": username, "status": "Authenticated"}, status=200)
    else:
        # 4. Generic error message for security
        return JsonResponse({"status": "Authentication failed"}, status=401) # 401 Unauthorized

def logout_request(request):
    username = ""
    if request.user.is_authenticated:
        username = request.user.username # Get username before logging out
    logout(request)
    # You might want to redirect to a specific page or return a more detailed JSON
    return JsonResponse({"userName": username, "status": "Logged out"})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Username already exists"}, status=409) # Use 409 Conflict
    
    try:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        return JsonResponse({"userName": username, "error": f"Registration failed: {e}"}, status=500)

# --- Dealer Views ---

# def get_dealerships(request, state="All"):
    # This view fetches dealers from a backend service.
    # Ensure `backend_url` is defined somewhere (e.g., in settings or passed)
    # Assuming 'get_request' is from .restapis and handles the actual API call
    # For now, let's use your existing local DB code if 'get_request' isn't set up.
    
    # If you are fetching from a backend service:
    # if state == "All":
    #     endpoint = "/fetchDealers"
    # else:
    #     endpoint = "/fetchDealers/" + state
    # dealerships = get_request(endpoint) # This would call your external API
    # return JsonResponse({"status": 200, "dealers": dealerships})

    # If you are fetching from your local Django DB (as per the commented out code below):
    # try:
    #     if state == "All":
    #         dealers = Dealer.objects.all().values('id', 'name', 'city', 'address', 'zip_state')
    #     else:
    #         # You would need a 'state' field in your Dealer model for this to work
    #         dealers = Dealer.objects.filter(state=state).values('id', 'name', 'city', 'address', 'zip_state')
    #     return JsonResponse(list(dealers), safe=False)
    # except Exception as e:
    #     logger.error(f"Error fetching dealerships: {e}")
    #     return JsonResponse({'error': 'Failed to retrieve dealerships'}, status=500)
    
    # # ibm gave hint

def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})


#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})



def dealership_list(request):
    # This view renders a template with a list of dealers from your local DB.
    dealers = Dealer.objects.all()
    print(f"Number of dealers fetched for template: {dealers.count()}")
    for dealer in dealers:
        print(f"Fetched dealer: {dealer.name}, ID: {dealer.id}")
    context = {
        'dealers': dealers,
    }
    return render(request, 'djangoapp/dealership_list.html', context)

def dealer_details(request, dealer_id):
    # View to display details for a specific dealership from your local DB.
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    context = {
        'dealer': dealer,
    }
    return render(request, 'djangoapp/dealer_details.html', context)

def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})
# def get_dealer_reviews(request, dealer_id):
#     # Assuming analyze_review_sentiments is implemented in .restapis
#     if dealer_id:
#         endpoint = "/fetchReviews/dealer/" + str(dealer_id)
#         reviews = get_request(endpoint) # Assuming this fetches reviews from a backend
#         if reviews: # Check if reviews is not None or empty
#             for review_detail in reviews:
#                 # Ensure 'review' key exists in review_detail before analyzing
#                 if 'review' in review_detail:
#                     sentiment_response = analyze_review_sentiments(review_detail['review'])
#                     review_detail['sentiment'] = sentiment_response.get('sentiment', 'N/A') # Use .get with default
#                 else:
#                     review_detail['sentiment'] = 'N/A (No review text)'
#         return JsonResponse({"status": 200, "reviews": reviews})
#     else:
#         return JsonResponse({"status": 400, "message": "Bad Request: No dealer_id provided"})

@csrf_exempt # Apply csrf_exempt if this is an API endpoint not using Django forms
def add_review(request, dealer_id): # This is the function `urls.py` expects
    if request.method == "POST":
        try:
            # Assuming you're sending JSON data from the frontend
            data = json.loads(request.body)
            # Add dealer_id to the data dictionary before posting
            data['dealer_id'] = dealer_id
            data['date'] = datetime.now().isoformat() # Use now() for current time

            # Assuming 'post_request' is from .restapis and handles the actual API call
            # This calls an *external* backend to insert the review.
            response = post_request("/insert_review", data) # Assuming your backend endpoint
            
            # Check the response from your backend service
            if response and response.get('status') == 200: # Adjust based on your backend's success response
                return JsonResponse({"status": 200, "message": "Review added successfully"}, status=200)
            else:
                return JsonResponse({"status": response.get('status', 500), "message": response.get('message', 'Failed to add review')}, status=response.get('status', 500))

        except json.JSONDecodeError:
            return JsonResponse({"status": 400, "message": "Invalid JSON format"}, status=400)
        except Exception as e:
            logger.error(f"Error adding review for dealer {dealer_id}: {e}")
            return JsonResponse({"status": 500, "message": f"Internal server error: {e}"}, status=500)
    else:
        return JsonResponse({"status": 405, "message": "Method Not Allowed"}, status=405)


# --- Car Views ---

def car_list(request):
    car_makes = CarMake.objects.all()
    car_models = CarModel.objects.all()
    context = {
        'car_makes': car_makes,
        'car_model': car_models, # Typo here, should be car_models
    }
    return render(request, 'djangoapp/car_list.html', context)

def get_cars(request):
    count = CarMake.objects.count() # Simpler way to get count
    if count == 0:
        initiate() # Populate if no cars exist
    
    car_models = CarModel.objects.select_related('car_make').all()
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})

# --- Initial Population ---
def populate(request):
    initiate()
    return HttpResponse("Database populated successfully.")




# # Uncomment the required imports before adding the code
# # encoder
# # Should be a json encoder class. Defaults to django.core.serializers.json.DjangoJSONEncoder.

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime
# import requests
# from .restapis import get_request


# from django.http import JsonResponse
# from django.contrib.auth import login, authenticate
# import logging
# import json
# from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate
# from .models import CarMake, CarModel
# from .models import Dealer
# import logging

# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Dealer # Assuming your model is named Dealer

# def post_review(data_dict):
#     request_url = backend_url+"/insert_review"
#     try:
#         response = requests.post(request_url,json=data_dict)
#         print(response.json())
#         return response.json()
#     except:
#         print("Network exception occurred")


# def get_dealer_reviews(request, dealer_id):
#     # if dealer id has been provided
#     if(dealer_id):
#         endpoint = "/fetchReviews/dealer/"+str(dealer_id)
#         reviews = get_request(endpoint)
#         for review_detail in reviews:
#             response = analyze_review_sentiments(review_detail['review'])
#             print(response)
#             review_detail['sentiment'] = response['sentiment']
#         return JsonResponse({"status":200,"reviews":reviews})
#     else:
#         return JsonResponse({"status":400,"message":"Bad Request"})




# #Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
# def get_dealerships(request, state="All"):
#     if(state == "All"):
#         endpoint = "/fetchDealers"
#     else:
#         endpoint = "/fetchDealers/"+state
#     dealerships = get_request(endpoint)
#     return JsonResponse({"status":200,"dealers":dealerships})


# # Create Django views to get dealers


# #Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
# def get_dealerships(request, state="All"):
#     if(state == "All"):
#         endpoint = "/fetchDealers"
#     else:
#         endpoint = "/fetchDealers/"+state
#     dealerships = get_request(endpoint)
#     return JsonResponse({"status":200,"dealers":dealerships})




# def dealer_details(request, dealer_id):
#     # View to display details for a specific dealership.
#     dealer = get_object_or_404(Dealer, pk=dealer_id)
#     context = {
#         'dealer': dealer,
#         # Add any other data you want to pass to the template
#     }
#     # return render(request, 'django/dealer_details.html', context)
#     return render(request, 'djangoapp/dealer_details.html', context)


# #adding the get_dealership function to my djangoapp/views.py
# #gemini help
# # def get_dealerships(request):
# #     if request.method == 'GET':
# #         try:
# #             dealers = Dealer.objects.all().values('id', 'name', 'city', 'address', 'zip_state')
# #             return JsonResponse(list(dealers), safe=False)
# #         except Exception as e:
# #             logger.error(f"Error fetching dealerships: {e}")
# #             return JsonResponse({'error: Failed to retrieve dealerships'}, status=500)
# #     else:
# #         return JsonResponse({'error': 'Only GET request are allowed.'}, status=450)

# def dealership_list(request):
#     dealers = Dealer.objects.all()
#     context = {
#         'dealers': dealers,
#     }
#     return render(request, 'djangoapp/dealership_list.html', context)
# # ++++++++================================================


# logger = logging.getLogger(__name__)

# def dealership_list(request):
#     dealers = Dealer.objects.all()
#     print(f"Number of dealers fetched: {dealers.count()}")  # Add this line
#     for dealer in dealers:
#         print(f"Fetched dealer: {dealer.name}, ID: {dealer.id}")  # Add this loop
#     context = {
#         'dealers': dealers,
#     }
#     return render(request, 'djangoapp/dealership_list.html', context)

# #this part adding for the get car and click on it
# def car_list(request):
#     car_makes = CarMake.objects.all()   # Get all CarMake objects
#     car_models = CarModel.objects.all() #  Get all CarModel objects
#     context = {
#         'car_makes': car_makes, 
#         'car_model': car_models,
#     }
#     return render(request, 'djangoapp/car_list.html', context)
 
# #  this part is the newest one not sure I should add it here
# def get_cars(request):
#     count = CarMake.objects.filter().count()
#     print(count)
#     if(count == 0):
#         initiate()
#     car_models = CarModel.objects.select_related('car_make')
#     cars = []
#     for car_model in car_models:
#         cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
#     return JsonResponse({"CarModels":cars})    



# # Get an instance of a logger
# logger = logging.getLogger(__name__)
# # =============
# def get_dealerships_json(request):
#     # ... (your existing get_dealerships function - I've renamed it) ...
#     if request.method == 'GET':
#         try:
#             dealers = Dealer.objects.all().values('id', 'name', 'city', 'address', 'zip_state')
#             return JsonResponse(list(dealers), safe=False)
#         except Exception as e:
#             logger.error(f"Error fetching dealerships: {e}")
#             return JsonResponse({'error: Failed to retrieve dealerships'}, status=500)
#     else:
#         return JsonResponse({'error': 'Only GET request are allowed.'}, status=450)

# def dealership_list(request):
#     dealers = Dealer.objects.all()
#     context = {
#         'dealers': dealers,
#     }
#     return render(request, 'djangoapp/dealership_list.html', context)

# def dealer_details(request, dealer_id):
#     # ... (your existing dealer_details function) ...
#     dealer = get_object_or_404(Dealer, pk=dealer_id)
#     context = {
#         'dealer': dealer,
#     }
#     return render(request, 'djangoapp/dealer_details.html', context)

# # ... (other views) ...================

# # Create your views here.

# # Create a `login_request` view to handle sign in request
# @csrf_exempt
# def login_user(request):
#     # Get username and password from request.POST dictionary
#     data = json.loads(request.body)
#     username = data['userName']
#     password = data['password']
#     # Try to check if provide credential can be authenticated
#     user = authenticate(username=username, password=password)
#     data = {"userName": username}
#     if user is not None:
#         # If user is valid, call login method to login current user
#         login(request, user)
#         data = {"userName": username, "status": "Authenticated"}
#     return JsonResponse(data)

# # Create a `logout_request` view to handle sign out request
# # def logout_request(request):  or def logout_view(request):
# # ...
# def logout_request(request):
#     logout(request)             #This clears the session data and logs out the user.
#     data = {"userName": ""}
#     return JsonResponse(data)


# # Create a `registration` view to handle sign up request
# # @csrf_exempt
# # def registration(request):
# # ...


# # @csrf_exempt
# # def registration(request):
# #     context = {}

# #     data = json.loads(request.body)
# #     username = data['userName']
# #     password = data['password']
# #     first_name = data['firstName']
# #     last_name = data['lastName']
# #     email = data['email']
# #     username_exist = False
# #     email_exist = False
# #     try:
# #         # Check if user already exists
# #         User.objects.get(username=username)
# #         username_exist = True
# #     except:
# #         # If not, simply log this is a new user
# #         logger.debug("{} is new user".format(username))

# #     # If it is a new user
# #     if not username_exist:
# #         # Create user in auth_user table
# #         user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
# #         # Login the user and redirect to list page
# #         login(request, user)
# #         data = {"userName":username,"status":"Authenticated"}
# #         return JsonResponse(data)
# #     else :
# #         data = {"userName":username,"error":"Already Registered"}
# #         return JsonResponse(data)
 
# @csrf_exempt
# def registration(request):
#     context = {}

#     data = json.loads(request.body)
#     username = data['userName']
#     password = data['password']
#     first_name = data['firstName']
#     last_name = data['lastName']
#     email = data['email']
#     username_exist = False
#     email_exist = False
#     try:
#         # Check if user already exists
#         User.objects.get(username=username)
#         username_exist = True
#     except:
#         # If not, simply log this is a new user
#         logger.debug("{} is new user".format(username))

#     # If it is a new user
#     if not username_exist:
#         # Create user in auth_user table
#         user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
#         # Login the user and redirect to list page
#         login(request, user)
#         data = {"userName":username,"status":"Authenticated"}
#         return JsonResponse(data)
#     else :
#         data = {"userName":username,"error":"Already Registered"}
#         return JsonResponse(data)




# # # Update the `get_dealerships` view to render the index page with
# # a list of dealerships
# # def get_dealerships(request):
# # ...

# # Create a `get_dealer_reviews` view to render the reviews of a dealer
# # def get_dealer_reviews(request,dealer_id):
# # ...

# # Create a `get_dealer_details` view to render the dealer details
# # def get_dealer_details(request, dealer_id):
# # ...

# # Create a `add_review` view to submit a review
# # def add_review(request):
# # ...



# #####################################################################################################

# # def logout_request(request):
# #     logout(request) 

# # In the logout_request(request) function, these two lines perform the following actions:
# # logout(request): This is a Django built-in function that logs out the user. When a user is logged out, their session is destroyed, and they are no longer authenticated. This function is typically used to clear the session and redirect the user to a login page or homepage after logging out.
# # request: This is the parameter passed to the logout_request function. It represents the HTTP request object that contains all the information about the current request, including session data, cookies, and other user-related data. This is required by the logout() function to identify which user to log out.
# # =================================================================================================


# #  data = {"userName": ""}
# # The line data = {"userName": ""} creates a dictionary in Python, where:
# # data is the variable name.
# # The dictionary contains one key-value pair:
# # "userName" is the key (a string).
# # "" is the value associated with the key. In this case, it is an empty string.
# # So, this dictionary represents an object with a userName field that has an empty string as its value. This could be used to store or pass information about a user, like a username, which is currently empty.

# # ------------------------------------------------------------------------

# # for log-out authentication from chatgpt

# # from django.contrib.auth import logout
# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt

# # @csrf_exempt  # Use only if you're not sending CSRF tokens from the frontend (e.g., APIs)
# # def logout_request(request):
# #     if request.method == "POST":  # Only allow POST requests
# #         if request.user.is_authenticated:  # Check if user is logged in
# #             logout(request)  # Logs out the user
# #             return JsonResponse({"success": True, "message": "User logged out successfully", "userName": ""})
# #         else:
# #             return JsonResponse({"success": False, "message": "No active session"})
# #     else:
# #         return JsonResponse({"success": False, "message": "Invalid request method"})

# # from django.contrib.auth import logout
# # from django.http import JsonResponse
# # from django.views.decorators.csrf import ensure_csrf_cookie

# # @ensure_csrf_cookie  # This ensures CSRF token is set for the session
# # def logout_view(request):
# #     if request.method == "POST":  # Only allow POST requests for security
# #         if request.user.is_authenticated:
# #             username = request.user.username  # Get the username before logging out
# #             logout(request)  # Logs out the user and clears session data
# #             return JsonResponse({"userName": username})
# #         else:
# #             return JsonResponse({"error": "No active session"}, status=400)
# #     else:
# #         return JsonResponse({"error": "Invalid request method"}, status=405)
# ############### ###########################  ####################################

# # from django.contrib.auth import logout
# # from django.http import JsonResponse

# # def logout_request(request):
# #     if request.method == "POST":
# #         if request.user.is_authenticated:
# #             logout(request)
# #             return JsonResponse({"success": True, "message": "User logged out successfully", "userName": ""})
# #         else:
# #             return JsonResponse({"success": False, "message": "No active session"})
# #     return JsonResponse({"success": False, "message": "Invalid request method"})
# # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ##############################

# #  login by chat gpt:

# # import logging
# # import json
# # from django.contrib.auth import authenticate, login
# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt

# # logger = logging.getLogger(__name__)

# # Create your views here.

# # Create a `login_request` view to handle sign in request
# # @csrf_exempt  # Optional, use if CSRF tokens aren't handled on frontend
# # def login_user(request):
# #     if request.method == "POST":
# #         try:
# #             # Get username and password from request body
# #             data = json.loads(request.body)
# #             username = data.get('userName')
# #             password = data.get('password')

# #             if not username or not password:
# #                 return JsonResponse({"error": "Username and password are required"}, status=400)

# #             # Try to authenticate the user
# #             user = authenticate(username=username, password=password)
# #             if user is not None:
# #                 # If user is valid, log in the user
# #                 login(request, user)
# #                 return JsonResponse({"userName": username, "status": "Authenticated"})
# #             else:
# #                 return JsonResponse({"error": "Invalid credentials"}, status=401)
# #         except json.JSONDecodeError:
# #             return JsonResponse({"error": "Invalid JSON format"}, status=400)
# #         except Exception as e:
# #             logger.error(f"Login error: {e}")
# #             return JsonResponse({"error": "Internal server error"}, status=500)
# #     else:
# #         return JsonResponse({"error": "Invalid request method"}, status=405)
# # =+++===================+++++++++++==================++++++++++++++++==================+++++++++++++====

# #Example of the  registration by the google ai
# # import hashlib

# # def register_user():
# #     username = input("Enter username: ")
# #     password = input("Enter password: ")
# #     email = input("Enter email: ")

# #     if not is_valid_username(username):
# #         print("Invalid username. Please use only alphanumeric characters and underscores.")
# #         return

# #     if not is_strong_password(password):
# #          print("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.")
# #          return
    
# #     if not is_valid_email(email):
# #         print("Invalid email format.")
# #         return

# #     hashed_password = hash_password(password)
# #     save_user(username, hashed_password, email)
# #     print("Registration successful!")

# # def is_valid_username(username):
# #     return username.isalnum() or "_" in username

# # def is_strong_password(password):
# #     if len(password) < 8:
# #         return False
# #     if not any(char.isupper() for char in password):
# #         return False
# #     if not any(char.islower() for char in password):
# #         return False
# #     if not any(char.isdigit() for char in password):
# #         return False
# #     return True
    
# # def is_valid_email(email):
# #      return "@" in email and "." in email
    
# # def hash_password(password):
# #     return hashlib.sha256(password.encode()).hexdigest()

# # def save_user(username, hashed_password, email):
# #     with open("users.txt", "a") as file:
# #         file.write(f"{username},{hashed_password},{email}\n")

# # register_user()
# # ===========================================================================================================
# # an other version: 
# # import hashlib
# # import os

# # def register_user(username, password):
# #     if os.path.exists('users.txt'):
# #         with open('users.txt', 'r') as file:
# #             for line in file:
# #                 u, _ = line.strip().split(':')
# #                 if u == username:
# #                     return False, "Username already exists."
# #     hashed_password = hashlib.sha256(password.encode()).hexdigest()
# #     with open('users.txt', 'a') as file:
# #         file.write(f"{username}:{hashed_password}\n")
# #     return True, "Registration successful."

# # def login_user(username, password):
# #      if os.path.exists('users.txt'):
# #         with open('users.txt', 'r') as file:
# #             for line in file:
# #                 u, h = line.strip().split(':')
# #                 if u == username:
# #                     hashed_password = hashlib.sha256(password.encode()).hexdigest()
# #                     if h == hashed_password:
# #                         return True, "Login successful."
# #                     else:
# #                         return False, "Incorrect password."
# #         return False, "User not found."
# #      else:
# #         return False, "No users registered."




# # def get_dealer_details(request, dealer_id):
# #     if(dealer_id):
# #         endpoint = "/fetchDealer/"+str(dealer_id)
# #         dealership = get_request(endpoint)
# #         return JsonResponse({"status":200,"dealer":dealership})
# #     else:
# #         return JsonResponse({"status":400,"message":"Bad Request"})


# # Create a get_dealer_details method which takes the dealer_id as a parameter in views.py and add a mapping urls.py. It will use the get_request you implemented in the restapis.py passing the /fetchDealer/<dealer id> endpoint.

# ######--------------------- clean-code ---------------------------------

# # import json
# # import logging
# # import requests
# # from datetime import datetime

# # from django.shortcuts import render, redirect, get_object_or_404
# # from django.http import JsonResponse, HttpResponse
# # from django.contrib.auth import login, logout, authenticate
# # from django.contrib.auth.models import User
# # from django.views.decorators.csrf import csrf_exempt

# # from .models import CarMake, CarModel, Dealer
# # from .populate import initiate
# # # from .restapis import get_request, analyze_review_sentiments, post_request

# # logger = logging.getLogger(__name__)


# # def login_user(request):
# #     if request.method == "POST":
# #         username = request.POST.get('username')
# #         password = request.POST.get('password')
# #         user = authenticate(username=username, password=password)
# #         if user:
# #             login(request, user)
# #             return redirect('djangoapp:index')
# #         else:
# #             return render(request, 'djangoapp/login.html', {'error': 'Invalid credentials'})
# #     return render(request, 'djangoapp/login.html')


# # def logout_request(request):
# #     logout(request)
# #     return redirect('djangoapp:index')


# # def registration(request):
# #     if request.method == 'POST':
# #         username = request.POST.get('username')
# #         password = request.POST.get('password')
# #         first_name = request.POST.get('first_name')
# #         last_name = request.POST.get('last_name')
# #         if User.objects.filter(username=username).exists():
# #             return render(request, 'djangoapp/registration.html', {'error': 'Username already exists'})
# #         user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
# #         login(request, user)
# #         return redirect('djangoapp:index')
# #     return render(request, 'djangoapp/registration.html')


# # def get_cars(request):
# #     cars = CarModel.objects.select_related('make').all()
# #     return render(request, 'djangoapp/car_list.html', {'cars': cars})


# # def car_list(request):
# #     cars = CarModel.objects.select_related('make').all()
# #     return render(request, 'djangoapp/car_list.html', {'cars': cars})


# # def dealer_details(request, dealer_id):
# #     dealer = get_object_or_404(Dealer, id=dealer_id)
# #     cars = CarModel.objects.filter(make=dealer)
# #     return render(request, 'djangoapp/dealer_details.html', {'dealer': dealer, 'cars': cars})


# # def dealership_list(request):
# #     dealerships = Dealer.objects.all()
# #     return render(request, 'djangoapp/dealership_list.html', {'dealerships': dealerships})


# # def get_dealerships(request, state="All"):
# #     if state == "All":
# #         dealerships = Dealer.objects.all()
# #     else:
# #         dealerships = Dealer.objects.filter(state=state)
# #     return render(request, 'djangoapp/index.html', {'dealerships': dealerships, 'selected_state': state})


# # def get_dealerships_json(request):
# #     dealerships = list(Dealer.objects.values())
# #     return JsonResponse({'dealerships': dealerships})


# # def get_dealer_reviews(request, dealer_id):
# #     try:
# #         # Replace with real get_request if needed
# #         url = f"http://localhost:8000/api/reviews/{dealer_id}"
# #         response = requests.get(url)
# #         reviews = response.json().get("reviews", [])
# #         return JsonResponse({'reviews': reviews})
# #     except Exception as e:
# #         logger.error(f"Error fetching reviews: {e}")
# #         return JsonResponse({'error': str(e)}, status=500)


# # @csrf_exempt
# # def post_review(request, dealer_id):
# #     if request.method == "POST":
# #         try:
# #             payload = json.loads(request.body)
# #             payload['dealer_id'] = dealer_id
# #             payload['date'] = datetime.utcnow().isoformat()
# #             url = "http://localhost:8000/api/post_review"
# #             response = requests.post(url, json=payload)
# #             return JsonResponse(response.json(), status=response.status_code)
# #         except Exception as e:
# #             logger.error(f"Error posting review: {e}")
# #             return JsonResponse({'error': str(e)}, status=500)
# #     return JsonResponse({'error': 'Only POST method allowed'}, status=405)


# # def populate(request):
# #     initiate()
# #     return HttpResponse("Database populated successfully.")



