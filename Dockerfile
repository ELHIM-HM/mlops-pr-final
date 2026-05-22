# Use the official, lightweight Python 3.10 image
FROM python:3.10-slim

# Prevent Python from writing .pyc files to disk and ensure console output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies, forcing the much smaller CPU-only version of PyTorch
# We remove 'git' and 'curl' requirements from the image to reduce attack surface
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Copy the entire project code into the container
COPY . .

# Explicitly copy artifacts if they aren't caught by the general COPY . .
# This ensures your model and validation data are physically inside the image
COPY storage/ /app/storage/
COPY datasets/ /app/datasets/

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose the port FastAPI will run on
EXPOSE 8000

# Tell Docker to run the entrypoint script when the container boots
CMD ["./entrypoint.sh"]