# FROM python:3.9.18-slim-bookworm


# WORKDIR /python-docker

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# COPY . .
# RUN ls
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]


# Use a slim Python image. 'buster' or 'bookworm' are Debian versions.
# '3.9-slim' is usually fine and points to a recent slim version.
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker's build cache.
# If requirements.txt doesn't change, this layer (and pip install) won't rebuild.
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# --- CRITICAL: Download NLTK data for SentimentIntensityAnalyzer ---
# This ensures 'vader_lexicon' is available in the image.
RUN python -m nltk.downloader vader_lexicon

# Copy the rest of your application code into the container
# This copies app.py, .env, etc.
COPY . .

# Explicitly expose the port your Flask application will listen on.
# Your app.py likely runs on port 5000, as per previous suggestions.
EXPOSE 5000

# Command to run the application using Gunicorn, a production-ready WSGI server.
# It binds to all network interfaces (0.0.0.0) on port 5000.
# 'app:app' means look for the 'app' Flask application instance within 'app.py'.
# Code Engine will also set a PORT environment variable, and your app.py
# is configured to read it. Gunicorn can also be configured to read it,
# but directly specifying 5000 here is fine if it matches EXPOSE and app.py's default.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]