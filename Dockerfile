# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org Flask openai

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV TAUTULLI_BASE_URL=""
ENV DISCORD_WEBHOOK_URL=""
ENV OPENAI_API_KEY=""
ENV TAUTULLI_API_KEY=""
# Run tautulli_webhook.py when the container launches
CMD ["python", "tautulli_webhook.py"]
