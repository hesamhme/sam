# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app
pip
# Copy the Python requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python code to the container
COPY main.py .

# Run the Python script when the container starts
CMD [ "python", "main.py" ]
