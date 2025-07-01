# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# def get_request(endpoint, **kwargs):
# Add code for get requests to back end

# def analyze_review_sentiments(text):
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments

# def post_review(data_dict):
# Add code for posting review


# The get_request method has two arguments, the endpoint to be requested, and a Python keyword arguments representing all URL parameters to be associated with the get call.
# This function calls GET method in requests library with a URL and any URL parameters such as dealerId

def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")



def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")

def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})
    

def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        # If any error occurs
        print("Network exception occurred")


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")

# In /Users/ariarostami/Desktop/IBM-Project/Car-Dealership/xrwvm-fullstack_developer_capstone/server/djangoapp/restapis.py

# ... (your existing imports and get_request, analyze_review_sentiments functions) ...

# Ensure 'requests' is imported
#import requests # Make sure this is uncommented or added

def post_request(data_dict):
    """
    Sends a POST request to the backend to submit a new review.

    Args:
        data_dict (dict): A dictionary containing the review data
                          (e.g., 'dealership', 'car_model', 'review', 'purchase', etc.).

    Returns:
        dict or None: The JSON response from the backend if successful, otherwise None.
    """
    request_url = backend_url + "/djangoapp/add_review" # Adjust the endpoint as needed
    print(f"POST to {request_url}")
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        print(f"POST successful: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network or API error occurred during POST: {e}")
        print("Could not post review.")
        return None
    except ValueError as e:
        print(f"Failed to decode JSON from POST response: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during POST: {e}")
        return None



# googel suggestion..
# import requests # UNCOMMENT THIS LINE
# import os
# from dotenv import load_dotenv

# load_dotenv()

# backend_url = os.getenv(
#     'backend_url', default="http://localhost:3030")
# sentiment_analyzer_url = os.getenv(
#     'sentiment_analyzer_url',
#     default="http://localhost:5050/")

# def analyze_review_sentiments(text):
#     """
#     Analyzes the sentiment of a given text by calling an external sentiment analysis API.

#     Args:
#         text (str): The review text to be analyzed.

#     Returns:
#         dict: A dictionary containing the sentiment analysis result if successful,
#               otherwise None.
#     """
#     if not text:
#         print("Error: No text provided for sentiment analysis.")
#         return None

#     request_url = sentiment_analyzer_url + "analyze/" + text
#     print(f"Sending sentiment analysis request to: {request_url}")

#     try:
#         response = requests.get(request_url)
#         response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

#         sentiment_data = response.json()
#         print(f"Sentiment analysis successful: {sentiment_data}")
#         return sentiment_data
#     except requests.exceptions.RequestException as e:
#         # This catches all network-related errors from the requests library
#         print(f"Network or API error occurred: {e}")
#         print("Could not retrieve sentiment analysis.")
#         return None
#     except ValueError as e:
#         # This catches errors if the response is not valid JSON
#         print(f"Failed to decode JSON from response: {e}")
#         print("Sentiment analysis response was not valid JSON.")
#         return None
#     except Exception as e:
#         # Catch any other unexpected errors
#         print(f"An unexpected error occurred: {e}")
#         return None