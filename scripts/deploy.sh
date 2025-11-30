#!/bin/bash
set -e

echo "🚀 Corporate Actions Demo Deployment Script"
echo "==========================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker daemon not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""

# Check if ports are available
echo "🔍 Checking if ports are available..."
for port in 3000 8000 3307; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "⚠️  Port $port is already in use. Please stop the service using this port."
        echo "   You can find what's using it with: lsof -i :$port"
        exit 1
    fi
done
echo "✅ All required ports are available"
echo ""

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose up -d --build

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Wait for backend to be healthy
echo "Checking backend health..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy"
        break
    fi
    attempt=$((attempt + 1))
    echo "   Attempt $attempt/$max_attempts - waiting for backend..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ Backend failed to start. Check logs with: docker-compose logs backend"
    exit 1
fi

echo ""
echo "✨ Deployment complete!"
echo ""
echo "📱 Access the application:"
echo "   Dashboard:  http://localhost:3000"
echo "   API:        http://localhost:8000"
echo "   API Docs:   http://localhost:8000/docs"
echo "   Health:     http://localhost:8000/health"
echo ""
echo "🎬 Demo workflow:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Create a dividend event for AAPL"
echo "   3. Watch it process in real-time (status changes: PENDING → PROCESSING → COMPLETED)"
echo "   4. Create a few more events to see metrics update"
echo "   5. Show the API docs at http://localhost:8000/docs"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f          # All services"
echo "   docker-compose logs -f backend  # Just backend"
echo "   docker-compose logs -f frontend # Just frontend"
echo ""
echo "🛑 Stop the demo:"
echo "   docker-compose down             # Stop services"
echo "   docker-compose down -v          # Stop and remove data"
echo ""
