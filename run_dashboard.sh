#!/bin/bash

# VinBank Chatbot Security Lab Dashboard Launcher
# Run this to start the interactive testing dashboard

set -e

echo "🔐 VinBank Chatbot Security Lab Dashboard"
echo "=========================================="
echo ""

# Get project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

# Check venv
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv .venv"
    exit 1
fi

# Activate venv
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check Streamlit
if ! pip list | grep -q streamlit; then
    echo "📥 Installing Streamlit..."
    pip install streamlit -q
fi

echo ""
echo "✅ Environment ready!"
echo ""
echo "Choose dashboard:"
echo "1. Basic Dashboard (no API calls)"
echo "2. Advanced Dashboard (with real agents)"
echo ""

read -p "Enter choice (1 or 2, default: 1): " choice
choice=${choice:-1}

if [ "$choice" == "1" ]; then
    echo ""
    echo "🚀 Starting Basic Dashboard..."
    echo "📱 Opening http://localhost:8501 in your browser..."
    echo "💡 Press Ctrl+C to stop the server"
    echo ""
    streamlit run chatbot_dashboard.py
elif [ "$choice" == "2" ]; then
    echo ""
    echo "Checking API configuration..."
    if grep -q "OPENROUTER_API_KEY=" .env 2>/dev/null && [ $(grep "OPENROUTER_API_KEY=" .env | cut -d= -f2 | wc -c) -gt 5 ]; then
        echo "✅ API keys configured"
        echo ""
        echo "🚀 Starting Advanced Dashboard..."
        echo "📱 Opening http://localhost:8501 in your browser..."
        echo "💡 Press Ctrl+C to stop the server"
        echo ""
        streamlit run chatbot_dashboard_advanced.py
    else
        echo "❌ OpenRouter API key not configured!"
        echo "Please set OPENROUTER_API_KEY in .env"
        exit 1
    fi
else
    echo "Invalid choice!"
    exit 1
fi
