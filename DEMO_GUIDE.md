# Corporate Action Processing Demo Guide

**Interview Preparation: Director, IT Product Management**

---

## Pre-Demo Checklist (Day Before)

- [ ] Run full deployment: `cd corporate-actions-demo && ./scripts/deploy.sh`
- [ ] Verify all services healthy: `docker-compose ps`
- [ ] Test creating events: `./scripts/create-sample-data.sh`
- [ ] Clear test data: `docker-compose down -v && ./scripts/deploy.sh`
- [ ] Practice demo 2-3 times with timer (aim for 8-10 minutes)
- [ ] Charge Mac mini, have backup power
- [ ] Test HDMI output if presenting on external display
- [ ] Have backup plan: Screenshots + recorded video

---

## Demo Flow (8-10 minutes)

### Opening (30 seconds)

**Say:**
"I've built a corporate action processing system that demonstrates how I'd modernize legacy mainframe systems using cloud-native architecture. This is a working application that showcases both product strategy and technical execution."

**Show:**
- Dashboard at http://localhost:3000
- Quick pan to show all three sections: form, metrics, events

---

### Part 1: Live Event Creation (2 minutes)

**Say:**
"Let me create a real corporate action event right now."

**Do:**
1. Fill out dividend form:
   - Symbol: AAPL
   - Amount: 0.24
   - Ex-date: [tomorrow's date]
   - Record date: [3 days from now]
   - Payment date: [1 week from now]
2. Click "Create Event"
3. Watch it appear in the event list with PENDING status

**Say (while it processes):**
"Notice the event immediately appears with PENDING status. Behind the scenes, the background processor picks it up, moves it to PROCESSING, simulates the work with a 1.5 second delay, and marks it COMPLETED. This demonstrates event-driven architecture with automatic retry logic."

4. Point to status changing: PENDING → PROCESSING → COMPLETED
5. Show it in the metrics (total events increased)

**Technical points to mention:**
- "The API validates input with Pydantic schemas"
- "MySQL stores the event with full audit trail"
- "Background processor uses retry logic - up to 3 attempts on failure"

---

### Part 2: Multiple Event Types (2 minutes)

**Say:**
"Let me show the other event types we support."

**Do:**
1. Create Stock Split:
   - Symbol: TSLA
   - Ratio: 1:3
   - Effective date: [2 weeks from now]
2. Create Merger:
   - Symbol: MSFT
   - Target: ATVI
   - Exchange ratio: 1.5
   - Cash component: 95.00

**Say:**
"These three event types cover the core corporate actions: dividends, stock splits, and mergers. The flexible JSON payload in MySQL means we can easily add new types like spin-offs or rights issues without schema changes."

**Show:**
- Filter events by status
- Show metrics updating in real-time
- Point to different chart visualizations

---

### Part 3: API Documentation (1.5 minutes)

**Say:**
"Everything you see is built on a production-grade REST API."

**Do:**
1. Open http://localhost:8000/docs
2. Scroll through endpoints
3. Show POST /events schema
4. Expand GET /events to show filters

**Say:**
"FastAPI gives us automatic OpenAPI documentation. Notice the schema validation, error handling, and pagination built in. This is the same API that the dashboard calls."

**Quick mention:**
- "Health check endpoint for monitoring"
- "Metrics endpoint for observability"
- "All responses include proper HTTP status codes"

---

### Part 4: Architecture Deep Dive (2 minutes)

**Say:**
"Let me walk through the architecture that makes this possible."

**Show (either slides or talk through):**

1. **API Layer**
   - "FastAPI with async support for high concurrency"
   - "Pydantic validation catches errors before they hit the database"
   - "OpenAPI docs auto-generated from code"

2. **Data Layer**
   - "MySQL 8 with JSON payload for flexibility"
   - "Indexed queries for performance"
   - "Immutable audit log - every state change recorded"

3. **Processing Layer**
   - "Background processor with automatic retry"
   - "Simulates real-world delays and occasional failures"
   - "Status progression: PENDING → PROCESSING → COMPLETED/FAILED"

4. **Presentation Layer**
   - "React with real-time updates via polling"
   - "Chart.js for metrics visualization"
   - "Responsive design"

5. **Infrastructure**
   - "Docker Compose for local development"
   - "Kubernetes manifests ready for production"
   - "Horizontal scaling with HPA"

**Show:**
- Docker Compose file: `docker-compose.yml`
- Backend structure: `backend/app/`
- Kubernetes manifests: `kubernetes/deployment.yaml`

---

### Part 5: Product Roadmap (2 minutes)

**Say:**
"Now let me show you how I'd prioritize features as a product manager."

**Show:**
- Open `roadmap/PRODUCT_ROADMAP.md`
- Scroll through Sprint 1 (MVP)
- Show Sprint 2-4 progression

**Highlight key points:**

**Sprint 2: Resilience**
- "Idempotency keys prevent duplicate processing"
- "Circuit breaker for downstream services"
- "Dead letter queue for failed events"
- "Prometheus metrics for Grafana dashboards"

**Sprint 3: Compliance**
- "Immutable audit log with cryptographic verification"
- "PII encryption at rest and in transit"
- "RBAC for fine-grained permissions"
- "This sprint is critical for financial services compliance"

**Sprint 4: Scale**
- "Kafka integration for true event streaming"
- "Horizontal pod autoscaling"
- "Database read replicas"
- "Redis caching for hot data"
- "This enables 10,000 events/minute"

**Say:**
"Notice how I've structured this as JIRA stories with acceptance criteria and story points. Each sprint builds on the last, balancing new features with technical debt."

---

### Closing (1 minute)

**Say:**
"This demo shows three things:

1. **Technical execution** - I can build production-quality systems using modern tech stacks
2. **Product thinking** - I understand how to prioritize features based on business value and risk
3. **Agile delivery** - I break work into iterative sprints with clear acceptance criteria

The architecture decisions map directly to the job requirements: MySQL, REST APIs, event-driven processing, Docker, Kubernetes, and Agile methodologies."

**Pause for questions**

---

## Backup Talking Points

### If asked about specific technologies:

**"Why FastAPI over Flask?"**
- Native async support scales better
- Automatic API docs reduce maintenance
- Type hints catch bugs at development time
- Growing ecosystem, better for greenfield projects

**"Why MySQL over PostgreSQL?"**
- Aligns with JD requirement
- JSON support covers our use case
- Excellent OLTP performance
- Widely supported in cloud providers

**"How would you handle database migrations?"**
- Alembic for schema versioning
- Blue-green deployments for zero downtime
- Backward-compatible changes only
- Comprehensive rollback plan

### If asked about product management:

**"How do you prioritize features?"**
- WSJF (Weighted Shortest Job First)
- Business value × urgency / implementation cost
- Stakeholder input + data analysis
- Balance quick wins with strategic initiatives

**"How do you handle technical debt?"**
- 30% sprint capacity allocated to debt
- Prioritize debt that blocks future features
- Make trade-offs transparent to stakeholders
- Track debt in backlog like any other work

**"How do you measure success?"**
- Functional: Uptime, processing time, error rate
- Technical: Test coverage, deployment frequency, MTTR
- Product: User satisfaction, feature adoption, time-to-value
- Business: Cost savings, revenue impact, competitive advantage

### If asked about compliance:

**"How do you ensure regulatory compliance?"**
- Immutable audit logs with chain of custody
- Encryption everywhere (at rest + in transit)
- RBAC with principle of least privilege
- Regular security audits and penetration testing
- SOC 2 Type II certification process
- Automated compliance checks in CI/CD

**"What about disaster recovery?"**
- Multi-AZ deployments for high availability
- Automated backups with point-in-time recovery
- Regular DR drills (quarterly)
- RTO: 1 hour, RPO: 15 minutes
- Runbooks for common failure scenarios

### If asked about scale:

**"How would you handle 10x traffic?"**
1. **Immediate (same day)**
   - Horizontal scaling with Kubernetes HPA
   - Increase replica count
   - Add database connection pooling

2. **Short-term (1 week)**
   - Database read replicas
   - Redis cache layer
   - CDN for static assets

3. **Long-term (1 month)**
   - Kafka for event streaming
   - Sharding strategy for database
   - Separate read/write services
   - Auto-scaling policies tuned

---

## Demo Recovery Scenarios

### If Docker fails to start:
1. Show pre-recorded screen recording
2. Walk through code in VS Code
3. Show architecture diagrams on slides

### If network is slow:
1. Use local-only mode (no external dependencies)
2. Show cached screenshots
3. Focus on code walkthrough

### If dashboard doesn't load:
1. Use API docs at /docs instead
2. Show curl commands creating events
3. Query database directly with MySQL client

---

## Practice Questions (Rehearse Answers)

1. "Walk me through a time you had competing priorities from multiple stakeholders."
2. "How do you balance technical debt with new features?"
3. "Describe your approach to gathering requirements."
4. "How do you measure product success?"
5. "Tell me about a product launch that didn't go as planned."
6. "How do you work with engineering teams?"
7. "What's your experience with Agile/Scrum/SAFe?"
8. "How do you stay current with technology trends?"

---

## Final Checklist (Morning Of)

- [ ] Mac mini fully charged
- [ ] Services running: `docker-compose ps` shows all healthy
- [ ] Browser tabs open: localhost:3000, localhost:8000/docs, roadmap file
- [ ] VS Code open with project
- [ ] Have water bottle
- [ ] Arrive 10 minutes early
- [ ] Breathe, smile, you've got this! 

---

## Post-Demo Next Steps

**If they want to see the code:**
"Happy to walk through any specific module. The backend is pure Python with type hints, frontend is React with hooks, infrastructure is declarative YAML."

**If they want to try it:**
"I can share the GitHub repo, or email you a zip file. It runs on any Mac or Linux with Docker installed. Full setup takes 2 minutes."

**If they ask about timeline:**
"I built this over a weekend - about 8 hours total. In a production setting with a team, the MVP would take 2-3 sprints with proper code review and testing."

---

**Good luck! You've prepared well and built something impressive.**
