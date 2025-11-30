# Quick Start Guide - Mac Mini Deployment

## Prerequisites

1. **Install Docker Desktop**
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop
   - Verify: Open Terminal and run `docker --version`

2. **Verify system requirements**
   - macOS 11 or later
   - 8GB RAM minimum (16GB recommended)
   - 10GB free disk space

## One-Command Deployment

```bash
cd corporate-actions-demo
./scripts/deploy.sh
```

That's it! The script will:
- Check Docker is installed and running
- Check required ports are available (3000, 8000, 3307)
- Build all containers
- Start MySQL, backend API, and frontend dashboard
- Wait for services to be healthy
- Show you access URLs

## Access the Application

Once deployed:
- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Create Sample Data (Optional)

```bash
./scripts/create-sample-data.sh
```

This creates sample events for all three types (DIVIDEND, STOCK_SPLIT, MERGER).

## Verify Deployment

```bash
# Check all services are running
docker-compose ps

# Should show 3 services: mysql, backend, frontend
# All should be "Up" and "healthy"

# View logs
docker-compose logs -f

# Press Ctrl+C to stop viewing logs
```

## Stop the Demo

```bash
# Stop services (keeps data)
docker-compose down

# Stop services and delete data
docker-compose down -v
```

## Troubleshooting

### Port Already in Use
```bash
# Find what's using the port
lsof -i :3000
lsof -i :8000
lsof -i :3307

# Kill the process or change the port in docker-compose.yml
```

### Services Not Starting
```bash
# Check logs for errors
docker-compose logs backend
docker-compose logs mysql

# Restart with fresh build
docker-compose down -v
docker-compose up -d --build
```

### Can't Access Dashboard
```bash
# Verify frontend is running
docker-compose logs frontend

# Check if port 3000 is accessible
curl http://localhost:3000

# Try accessing from browser: http://localhost:3000
```

## Demo Day Checklist

The morning of your interview:

1. Start services: `./scripts/deploy.sh`
2. Verify access: Open http://localhost:3000 in browser
3. Create test event to confirm everything works
4. Clear test data: `docker-compose down -v && ./scripts/deploy.sh`
5. Review `DEMO_GUIDE.md` for talking points
6. Open browser tabs:
   - http://localhost:3000 (dashboard)
   - http://localhost:8000/docs (API docs)
   - `roadmap/PRODUCT_ROADMAP.md` in text editor
7. Have VS Code open with project
8. You're ready!

## Project Structure

```
corporate-actions-demo/
├── README.md              # Project overview
├── DEMO_GUIDE.md         # Complete demo script with timing
├── docker-compose.yml    # Service orchestration
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Config, database
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   ├── tests/           # Pytest suite
│   └── Dockerfile
├── frontend/            # React dashboard
│   ├── src/
│   │   ├── components/  # React components
│   │   └── services/    # API client
│   └── Dockerfile
├── kubernetes/          # K8s manifests
├── roadmap/            # Product roadmap
│   └── PRODUCT_ROADMAP.md
└── scripts/            # Deployment scripts
    ├── deploy.sh
    └── create-sample-data.sh
```

## Support

If you encounter issues:
1. Check `DEMO_GUIDE.md` for recovery scenarios
2. Review service logs: `docker-compose logs [service]`
3. Restart fresh: `docker-compose down -v && ./scripts/deploy.sh`

**You've got this! The demo is solid and you're well-prepared.**
