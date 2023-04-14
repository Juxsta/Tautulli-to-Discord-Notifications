# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy only the poetry.lock and pyproject.toml files into the container at /app
COPY poetry.lock pyproject.toml ./

# Install project dependencies from poetry.lock
RUN pip install --trusted-host pypi.python.org poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the main.py file into the container at /app
COPY main.py ./

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables
ENV DISCORD_WEBHOOK_URL=""
ENV OPENAI_API_KEY=""

# Run main.py when the container launches
CMD ["python", "main.py"]
