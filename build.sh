#!/bin/bash
set -o errexit

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
cd backend
python manage.py collectstatic --noinput --clear
cd ..

echo "Running database migrations..."
cd backend
python manage.py migrate --noinput
cd ..

echo "Seeding demo data..."
cd backend
python manage.py seed_demo_data || echo "Warning: seed_demo_data failed (may already exist)"
cd ..

echo "✅ Build complete!"
