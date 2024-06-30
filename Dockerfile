# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir fastapi uvicorn aiofiles

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for the markdown directory
ENV MARKDOWN_DIR '/app/mock documents'

# Create the markdown directory
RUN mkdir -p $MARKDOWN_DIR

# Run the FastAPI app when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]