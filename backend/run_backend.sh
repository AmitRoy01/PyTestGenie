#!/bin/bash
echo "========================================"
echo "  PyTestGenie - Unified Application"
echo "========================================"
echo ""
echo "Starting Backend Server..."
cd backend
python app_unified.py &
BACKEND_PID=$!
echo "Backend started on http://localhost:5000 (PID: $BACKEND_PID)"
echo ""
echo "Please start frontend separately with:"
echo "  cd frontend"
echo "  npm install"
echo "  npm run dev"
echo ""
echo "Press Ctrl+C to stop the backend server"
wait $BACKEND_PID
