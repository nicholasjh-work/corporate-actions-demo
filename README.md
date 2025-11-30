# Corporate Action Processing Demo

Real-time corporate action event processing system demonstrating modern cloud-native architecture for financial services.

## Architecture

- **API Layer**: FastAPI REST endpoints with OpenAPI documentation
- **Data Layer**: MySQL 8 for event persistence with proper indexing
- **Processing Layer**: Async event processor with retry logic
- **Presentation Layer**: React dashboard with real-time metrics
- **Infrastructure**: Docker Compose for local, Kubernetes manifests for production

## Tech Stack

- Python 3.11 (FastAPI, SQLAlchemy, MySQL Connector)
- MySQL 8
- React 18 with Chart.js
- Docker & Docker Compose
- Kubernetes (deployment manifests)

## Quick Start

```bash
# Prerequisites: Docker Desktop installed and running

# 1. Start the stack
docker-compose up -d

# 2. Wait for services to be healthy (30 seconds)
docker-compose ps

# 3. Access the application
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Dashboard: http://localhost:3000
# Health: http://localhost:8000/health

# 4. Create sample events
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "DIVIDEND",
    "symbol": "AAPL",
    "amount": 0.24,
    "ex_date": "2024-11-15",
    "record_date": "2024-11-18",
    "payment_date": "2024-11-25"
  }'

# 5. View metrics
curl http://localhost:8000/api/v1/metrics

# 6. Stop the stack
docker-compose down
```

## Demo Script

### Introduction (1 min)
"I've built a corporate action processing system that demonstrates how I'd modernize legacy mainframe systems using cloud-native architecture."

### Live Demo (3 min)
1. Show API documentation at /docs
2. Create a dividend event via API
3. Show event appears in dashboard with status progression
4. Create a stock split event
5. Show metrics aggregation in real-time

### Technical Deep Dive (2 min)
1. Explain event-driven architecture
2. Show resilience patterns (retry, idempotency)
3. Discuss scaling strategy with Kubernetes
4. Walk through compliance hooks (audit logs, immutability)

### Product Roadmap (2 min)
1. Show JIRA-style backlog
2. Discuss prioritization framework
3. Explain next 3 sprints of features

## Project Structure

```
corporate-actions-demo/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Config, database
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI application
│   ├── tests/            # Pytest test suite
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API client
│   │   └── App.jsx
│   ├── Dockerfile
│   └── package.json
├── kubernetes/           # K8s deployment manifests
├── roadmap/             # Product roadmap deck
├── docker-compose.yml
└── README.md
```

## Product Roadmap Highlights

### Sprint 1 (MVP - Current)
- ✅ Real-time event ingestion via REST API
- ✅ MySQL persistence with audit trail
- ✅ Basic event processor with status tracking
- ✅ Metrics dashboard

### Sprint 2 (Resilience)
- Idempotency keys for duplicate detection
- Dead letter queue for failed events
- Circuit breaker for downstream services
- Prometheus metrics export

### Sprint 3 (Compliance)
- Immutable audit log with chain of custody
- PII data encryption at rest
- Role-based access control (RBAC)
- Regulatory reporting APIs

### Sprint 4 (Scale)
- Kafka integration for event streaming
- Horizontal pod autoscaling
- Database read replicas
- Cache layer with Redis

## Compliance Considerations

- **Audit Trail**: Every event mutation logged with timestamp and user
- **Data Retention**: 7-year retention policy configurable
- **Immutability**: Events cannot be deleted, only marked cancelled
- **Encryption**: Database encryption at rest, TLS in transit
- **Access Control**: API key authentication, role-based permissions

## Monitoring & Observability

- Health check endpoint: `/health`
- Metrics endpoint: `/api/v1/metrics`
- Structured JSON logging
- Request tracing with correlation IDs
- Database query performance logging

## Testing

```bash
cd backend
pytest tests/ -v --cov=app --cov-report=term-missing
```

Coverage target: >80%

## Production Deployment

See `kubernetes/` directory for deployment manifests.

Key production considerations:
- Use managed MySQL (RDS, Cloud SQL)
- External secrets management (Vault, AWS Secrets Manager)
- Horizontal pod autoscaling based on CPU/memory
- Ingress with TLS termination
- Persistent volume claims for logs

## Questions to Prepare For

1. **How would you handle 10x traffic spike?**
   - Horizontal scaling with K8s HPA
   - Database read replicas
   - Redis cache for hot data
   - Rate limiting at API gateway

2. **What about data consistency?**
   - Database transactions with proper isolation
   - Idempotency keys
   - Event sourcing for audit trail

3. **How do you ensure compliance?**
   - Immutable audit logs
   - Data encryption
   - Access control
   - Regular security audits

4. **What's the migration strategy from mainframe?**
   - Parallel run period
   - Data reconciliation
   - Gradual traffic shift
   - Rollback plan

## License

Demo project for interview purposes.
