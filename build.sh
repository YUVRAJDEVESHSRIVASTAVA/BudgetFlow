#!/bin/bash
set -o errexit

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "Collecting static files..."
cd backend
python manage.py collectstatic --noinput

echo "Running database migrations..."
python manage.py migrate

echo "Seeding demo data..."
python manage.py seed_demo_data

echo "Build complete!"
