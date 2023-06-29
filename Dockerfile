# Use the official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port your Flask app will run on
EXPOSE 5000

# Define the command to run your Flask app
CMD ["python", "app.py"]