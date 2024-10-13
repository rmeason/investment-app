# Base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Update pip to the latest version
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port the app will run on
EXPOSE 5000

# Command to run the app
CMD ["python", "run.py"]