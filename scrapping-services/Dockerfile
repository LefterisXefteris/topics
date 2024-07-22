# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Specify the command to run on container start
CMD ["python", "app.py"]