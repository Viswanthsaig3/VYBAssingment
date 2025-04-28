# Build frontend
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Python backend
FROM python:3.10-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY *.py .env ./
COPY cache/ ./cache/

# Copy frontend build
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
