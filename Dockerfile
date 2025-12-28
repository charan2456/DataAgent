FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy backend and real_agents directories
COPY backend ./backend
COPY real_agents ./real_agents

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install pyecharts
RUN pip install --no-cache-dir pyecharts

# Set environment variables
ENV VARIABLE_REGISTER_BACKEND=redis \
    MESSAGE_MEMORY_MANAGER_BACKEND=database \
    JUPYTER_KERNEL_MEMORY_MANAGER_BACKEND=database \
    FLASK_APP=backend.main

# Create data directory
RUN mkdir -p /app/backend/data

# Expose port
EXPOSE 8000

# Run Flask app
CMD ["python", "-m", "flask", "run", "-p", "8000", "--host", "0.0.0.0"]

