### PROD ###
FROM python:3.11-slim-buster as prod
RUN apt-get update
# Set the working directory to /app
WORKDIR /app

COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Run app.py when the container launches
CMD ["python", "-m", "src"]
