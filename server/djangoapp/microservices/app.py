# from flask import Flask
# from nltk.sentiment import SentimentIntensityAnalyzer
# import json
# app = Flask("Sentiment Analyzer")

# sia = SentimentIntensityAnalyzer()


# @app.get('/')
# def home():
#     return "Welcome to the Sentiment Analyzer. \
#     Use /analyze/text to get the sentiment"


# @app.get('/analyze/<input_txt>')
# def analyze_sentiment(input_txt):

#     scores = sia.polarity_scores(input_txt)
#     print(scores)
#     pos = float(scores['pos'])
#     neg = float(scores['neg'])
#     neu = float(scores['neu'])
#     res = "positive"
#     print("pos neg nue ", pos, neg, neu)
#     if (neg > pos and neg > neu):
#         res = "negative"
#     elif (neu > neg and neu > pos):
#         res = "neutral"
#     res = json.dumps({"sentiment": res})
#     print(res)
#     return res


# if __name__ == "__main__":
#     app.run(debug=True)


#  new version suggested by the gemini 


from flask import Flask, request, jsonify
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file (if it exists) for local development
# In Code Engine, environment variables are set directly, so .env won't be used there.
load_dotenv()

# --- NLTK Data Download (Crucial for Deployment) ---
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    print("VADER lexicon not found, downloading...")
    nltk.download('vader_lexicon')
    print("VADER lexicon downloaded.")

sia = SentimentIntensityAnalyzer()

app = Flask("Sentiment Analyzer")

@app.route('/')
def home():
    return "Welcome to the Sentiment Analyzer. Use /analyze to get the sentiment using a POST request with JSON."

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "No 'text' provided in the request body"}), 400
    
    if not isinstance(text, str):
        return jsonify({"error": "'text' field must be a string"}), 400

    scores = sia.polarity_scores(text)
    compound_score = scores['compound']

    if compound_score >= 0.05:
        sentiment = "positive"
    elif compound_score <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return jsonify({
        "input_text": text,
        "sentiment_scores": scores,
        "overall_sentiment": sentiment
    })

if __name__ == "__main__":
    # Get port from environment variable, default to 5000
    # This PORT env var will be set by Docker Compose or Code Engine
    port = int(os.environ.get('PORT', 5000)) 
    app.run(host='0.0.0.0', port=port, debug=True)








# # and only for mini project for the flask this suggestion from the gemini and if want to have code engine locally and test our code.
# from flask import Flask, request, jsonify
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer
# import os # Import os module to check for environment variables

# # --- NLTK Data Download (Crucial for Deployment) ---
# # Ensure NLTK data is downloaded. This is important for Docker.
# # This check will attempt to download if not present.
# # In a Dockerfile, you'd typically run 'python -m nltk.downloader vader_lexicon'
# # or handle it in your entrypoint script.
# try:
#     nltk.data.find('sentiment/vader_lexicon.zip')
# except nltk.downloader.DownloadError:
#     print("VADER lexicon not found, downloading...")
#     nltk.download('vader_lexicon')
#     print("VADER lexicon downloaded.")

# sia = SentimentIntensityAnalyzer()

# app = Flask("Sentiment Analyzer")

# @app.route('/')
# def home():
#     return "Welcome to the Sentiment Analyzer. \
#     Use /analyze to get the sentiment using a POST request with JSON."

# # Changed to POST for better API practice with JSON input
# @app.route('/analyze', methods=['POST'])
# def analyze_sentiment():
#     if not request.is_json:
#         return jsonify({"error": "Request must be JSON"}), 400

#     data = request.get_json()
#     text = data.get('text')

#     if not text:
#         return jsonify({"error": "No 'text' provided in the request body"}), 400
    
#     # Ensure text is a string
#     if not isinstance(text, str):
#         return jsonify({"error": "'text' field must be a string"}), 400

#     scores = sia.polarity_scores(text)
    
#     # Extract scores
#     compound_score = scores['compound'] # This is often the most useful VADER score

#     # Define sentiment based on compound score
#     # VADER typically uses a compound score threshold
#     # You can adjust these thresholds if your requirements differ
#     if compound_score >= 0.05:
#         sentiment = "positive"
#     elif compound_score <= -0.05:
#         sentiment = "negative"
#     else:
#         sentiment = "neutral"

#     # Return a more comprehensive JSON response
#     return jsonify({
#         "input_text": text,
#         "sentiment_scores": scores, # Include all VADER scores for more detail
#         "overall_sentiment": sentiment
#     })

# if __name__ == "__main__":
#     # Get port from environment variable, default to 5000
#     port = int(os.environ.get('PORT', 5000)) 
#     # Use 0.0.0.0 to make it accessible from outside the container
#     app.run(host='0.0.0.0', port=port, debug=True)
#_____++++++++++++++++++++++++++++++++++**************************