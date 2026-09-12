# Python ka official lightweight image use karenge
FROM python:3.10-slim

# Working directory set karein
WORKDIR /app

# System dependencies install karein (database aur package compilation ke liye)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Requirements file copy karein aur libraries install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Poora project code copy karein
COPY . .

# Flask app ka port expose karein
EXPOSE 5000

# Gunicorn ke zariye app run karne ki command (Production ready)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]