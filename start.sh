#!/bin/bash

echo "🎮 Starting Tic Tac Toe Multiplayer Server..."
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "🚀 Starting server..."
echo ""
echo "Access the game at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
