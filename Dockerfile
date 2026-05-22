# Use the official, lightweight Python 3.10 image
FROM python:3.10-slim

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ==========================================
# DEVOPS MAGIC: Tell Python where to find our code
ENV PYTHONPATH=/app
# ==========================================

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Copy the entire project code into the container
COPY . .

# Explicitly copy artifacts
COPY storage/ /app/storage/
COPY datasets/ /app/datasets/

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose the port FastAPI will run on
EXPOSE 8000

# Tell Docker to run the entrypoint script when the container boots
CMD ["./entrypoint.sh"]