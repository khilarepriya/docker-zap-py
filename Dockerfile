FROM python:3.9

# Copy source code
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn to replace Flask dev server
RUN pip install gunicorn

# Expose Flask app port
EXPOSE 5020

# Run app with gunicorn to avoid Werkzeug Server header
CMD ["gunicorn", "--bind", "0.0.0.0:5020", "app:app"]

