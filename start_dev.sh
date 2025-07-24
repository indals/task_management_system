#!/bin/bash

# Development startup script for Flask Task Management System

echo "🚀 Starting Flask Task Management System..."

# Activate virtual environment
source venv/bin/activate

# Set Flask environment variables
export FLASK_APP=run.py
export FLASK_ENV=development
export FLASK_DEBUG=1

echo "✅ Virtual environment activated"
echo "✅ Flask environment variables set"
echo ""
echo "Available commands:"
echo "  flask run                    - Start development server"
echo "  flask db upgrade            - Apply database migrations"
echo "  flask db migrate -m 'msg'   - Create new migration"
echo "  flask shell                 - Open Flask shell"
echo "  flask routes                - Show all routes"
echo ""
echo "Database health check:"
curl -s http://localhost:5000/api/health/db 2>/dev/null || echo "Server not running yet"
echo ""
echo "To start the server: flask run --host=0.0.0.0 --port=5000"