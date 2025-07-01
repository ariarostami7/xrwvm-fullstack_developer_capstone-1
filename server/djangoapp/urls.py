# In djangoapp/urls.py (or your project's urls.py if that's where it is)

from django.urls import path
from . import views # THIS IS IMPORTANT: ensures you're importing from your app's views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your existing paths ...
    # Path for adding a review
    # The URL pattern should capture the dealer_id as an integer
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),
    # You might also have this for viewing reviews (if not already there):
    path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='get_dealer_reviews'),
    # And for dealer details:
    path('dealer/<int:dealer_id>/', views.dealer_details, name='dealer_details'),

    # Other paths like login, logout, registration, get_dealerships, etc.
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('dealerships/', views.dealership_list, name='dealership_list'), # For template rendering
    path('api/dealerships/', views.get_dealerships, name='get_dealerships_api'), # For JSON API
    path('api/dealerships/<str:state>/', views.get_dealerships, name='get_dealerships_by_state_api'),
    path('api/dealers/', views.get_dealerships, name='get_dealerships'),
    path('cars/', views.car_list, name='car_list'),
    path('api/cars/', views.get_cars, name='get_cars_api'),
    path('populate/', views.populate, name='populate'), # For initial data population
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    path(route='add_review', view=views.add_review, name='add_review'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



# # Uncomment the imports before you add the code
# from django.urls import path
# from django.conf.urls.static import static
# from django.conf import settings
# from . import views
# from .restapis import get_request, analyze_review_sentiments, post_review

# app_name = 'django-app'
# urlpatterns = [
#     # # path for registration
#     # path(route='Register', view=views.register, name='register'),
#     path(route='Register', view=views.registration, name='register'),
#     # path for login
#     path(route='login', view=views.login_user, name='login'),

#     #path for logout
#     path(route='logout', view=views.logout_request, name='logout'),
    
#     # path for dealer reviews view
#     # path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),

# #    # using gemini   suggesting something else;
# #     # path('get_dealers/', views.get_dealerships, name='get_dealers'),
# #     path('get_dealers/', views.get_dealerships_json, name='get_dealers_json'), # Renamed for clarity
# #     path('dealers/', views.dealership_list, name='dealership_list'),       # New path for the HTML list
# #     path('dealer/<int:dealer_id>/', views.dealer_details, name='dealer_details'),

#     # API endpoint for fetching all dealerships (for React)
#     # path('api/dealers/', views.get_dealerships_json, name='get_dealers_json'),
#     path('api/dealers/', views.get_dealerships_json, name='get_dealerships_json'),

#     # HTML page to list dealerships (if you still need this)
#     path('dealers/', views.dealership_list, name='dealership_list'),

#     path('dealer/<int:dealer_id>/', view=views.dealer_details, name='dealer_details'),

    
#     path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
#     path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
#     path("dealer/<int:dealer_id>/add_review", views.post_review, name="add_review"),
#     # path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),


#     # path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'), extra


#     # path for add a review view

#     # path for add get_cars 
#     # New part 
#     path('cars/', views.car_list, name='car_list'),
#     path(route='get_cars', view=views.get_cars, name ='getcars'),
#     path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
#     path(route='add_review', view=views.add_review, name='add_review'),

#     #NEW PART APPEND "/"
#     # path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
#     # NEW PATH FOR DEALER DETAIL VIEW "gemini help"
#     # path('dealer/<int:dealer_id>/', views.dealer_details, name='dealer_details'),
#     ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    

# # Uncomment the imports before you add the code
# # from django.urls import path
# # from django.conf.urls.static import static
# # from django.conf import settings
# # from . import views


# # app_name = 'django-app'
# # urlpatterns = [ 
# #     # path for login
# #     path('login/', views.login_user, name='login'),

# #     # path for logout
# #     path('logout/', views.logout_request, name='logout'),

# #     # path for dealer reviews view (you might have a specific view for this later)
# #     # path('dealer_reviews/', views.dealer_reviews, name='dealer_reviews'),

# #     # API endpoint to get dealerships as JSON
# #     path('api/dealers/', views.get_dealerships_json, name='get_dealers_json'),

# #     # HTML page to list dealerships
# #     # path('dealers/', views.dealership_list, name='dealership_list'),

# #     # HTML page for individual dealer details
# #     path('dealer/<int:dealer_id>/', views.dealer_details, name='dealer_details'),

# #     # path for car list view
# #     path('cars/', views.car_list, name='car_list'),

# #     # API endpoint to get cars as JSON
# #     path('api/cars/', views.get_cars, name='getcars'),

# #     # You had these commented out or duplicated, I've removed the extra ones:
# #     # path(route='Register', view=views.register, name='register'),
# #     # path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
# #     # path(route='get_cars', view=views.get_cars, name ='getcars'),
# #     # path('dealer/int:dealer_id>/', views.dealer_details, name='dealer_details'),
# # ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# # clean way of the code 

# # from django.urls import path
# # from django.conf.urls.static import static
# # from django.conf import settings
# # from . import views
# # from .restapis import get_request, analyze_review_sentiments, post_review

# # app_name = 'django-app'

# # urlpatterns = [
# #     # Authentication routes
# #     path('Register/', view=views.registration, name='register'),  # Consider lowercase: 'register/'
# #     path('login/', view=views.login_user, name='login'),
# #     path('logout/', view=views.logout_request, name='logout'),

# #     # Dealership views
# #     path('dealers/', views.dealership_list, name='dealership_list'),                      # HTML list page
# #     path('dealer/<int:dealer_id>/', views.dealer_details, name='dealer_details'),         # Dealer detail page

# #     # API: Get all dealers and by state
# #     path('api/dealers/', views.get_dealerships_json, name='get_dealerships_json'),        # JSON for frontend
# #     path('get_dealers/', view=views.get_dealerships, name='get_dealers'),                 # Optional, might overlap
# #     path('get_dealers/<str:state>/', view=views.get_dealerships, name='get_dealers_by_state'),

# #     # Car views
# #     path('cars/', views.car_list, name='car_list'),
# #     path('get_cars/', views.get_cars, name='getcars'),

# #     # Review routes
# #     path('reviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),
# #     path('add_review/', views.add_review, name='add_review'),
    
# # ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


