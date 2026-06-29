# Tracker v2.0

## Overview

**Tracker** is an email intelligence platform that automatically organizes job applications from Gmail. It combines rule‑based processing with machine‑learning classification to provide a scalable, production‑ready solution.

---

## Table of Contents

- [Vision](#vision)
- [Roadmap](#roadmap)
  - [Sprint 0 – Architecture Planning](#sprint-0---architecture-planning)
  - [Sprint 1 – Email Processing Pipeline](#sprint-1---email-processing-pipeline)
  - [Sprint 2 – Gmail Infrastructure](#sprint-2---gmail-infrastructure)
  - [Sprint 3 – Database Redesign](#sprint-3---database-redesign)
  - [Sprint 4 – Service Layer](#sprint-4---service-layer)
  - [Sprint 5 – Repository Pattern](#sprint-5---repository-pattern)
  - [Sprint 6 – Background Processing](#sprint-6---background-processing)
  - [Sprint 7 – Review Queue (Human‑in‑the‑Loop)](#sprint-7---review-queue-human-in-the-loop)
  - [Sprint 8 – ML Improvements](#sprint-8---ml-improvements)
  - [Sprint 9 – Analytics Engine](#sprint-9---analytics-engine)
  - [Sprint 10 – Production Readiness](#sprint-10---production-readiness)
  - [Sprint 11 – Frontend Integration](#sprint-11---frontend-integration)
  - [Sprint 12 – Deployment](#sprint-12---deployment)
- [Stretch Goals](#stretch-goals)
- [Estimated Timeline](#estimated-timeline)

---

## Vision

Build a production‑ready platform that automatically extracts, classifies, and tracks job‑application emails from Gmail, leveraging a hybrid **rules + ML** pipeline, robust background processing, and a clean analytics dashboard.

---

## Roadmap

### Sprint 0 — Architecture Planning

**Duration:** 1 day

- Define overall backend architecture
- Define email processing pipeline
- Design classification workflow
- Design database architecture
- Design service & repository layers
- Draw system architecture diagram
- Document all architectural decisions

---

### Sprint 1 — Email Processing Pipeline

**Duration:** 3–4 days

#### Target Architecture

```javascript
Gmail → Email Parser → Spam Filter → Job Alert Filter → Rule Engine → ML Classifier → Decision Engine → Database
```

#### Tasks

- **Pipeline**
  - Create `pipeline.py`
  - Create `PipelineResult`
  - Remove business logic from routes
- **Filters**
  - Spam Filter
  - Job Alert Filter
  - Company Newsletter Filter
  - Duplicate Email Filter
- **Rule Engine**
  - Rejection Rules
  - Offer Rules
  - Interview Rules
  - Assessment Rules
  - Application Confirmation Rules
- **ML Layer**
  - ML as fallback only
  - Confidence calibration
  - Threshold tuning
  - Prediction metadata
- **Decision Engine**
  - SAVE
  - IGNORE
  - NEEDS\_REVIEW
  - UPDATE\_EXISTING

---

### Sprint 2 — Gmail Infrastructure

**Duration:** 3 days

- **OAuth**
  - Refresh tokens
  - Handle expired tokens
  - Multi‑account support
  - Retry failed authentication
- **Sync**
  - Pagination
  - Incremental sync
  - Sync only new emails
  - Resume interrupted sync
  - Retry failed emails
- **Performance**
  - Batch Gmail API calls
  - Batch database writes
  - Sync progress tracking
  - Sync statistics

---

### Sprint 3 — Database Redesign

**Duration:** 2–3 days

- **Tables**
  - `email_messages`
  - `job_applications`
  - `gmail_tokens`
  - `sync_history`
- **Metadata**
  - confidence
  - classification\_method
  - pipeline\_stage
  - processing\_time
  - processed\_at
- **Relationships**
  - Email → Application
  - Thread tracking
  - Status history

---

### Sprint 4 — Service Layer

**Duration:** 2 days

- **Create Services**
  - GmailService
  - SyncService
  - AnalyticsService
  - ApplicationService
- **Refactor**
  - Gmail logic
  - CRUD logic
  - Analytics logic
  - Email processing logic

---

### Sprint 5 — Repository Pattern

**Duration:** 2 days

- **Repositories**
  - ApplicationRepository
  - GmailRepository
  - TokenRepository
- **Methods**
  - `save_application()`
  - `update_application()`
  - `find_by_message_id()`
  - `find_by_thread()`
  - `delete_application()`
  - `statistics()`

---

### Sprint 6 — Background Processing

**Duration:** 4 days

- **Tasks**
  - Background worker
  - Job queue
  - Progress API
  - Cancel sync
  - Retry failed jobs
- **Future Options**
  - APScheduler
  - Celery
  - Redis Queue

---

### Sprint 7 — Review Queue (Human‑in‑the‑Loop)

**Duration:** 3 days

- **Tasks**
  - Needs‑review endpoint
  - Review UI
  - Accept prediction
  - Correct prediction
  - Store corrections
  - Auto‑generate training dataset

---

### Sprint 8 — ML Improvements

**Duration:** 4–5 days

- **Dataset**
  - Collect real emails
  - Build review dataset
  - Reduce synthetic bias
- **Features**
  - Subject weighting
  - Sender weighting
  - HTML cleanup
  - Signature removal
- **Model**
  - Retrain logistic regression
  - Cross‑validation
  - Probability calibration
  - Threshold optimization
- **Metrics**
  - Precision
  - Recall
  - F1 score
  - Confusion matrix

---

### Sprint 9 — Analytics Engine

**Duration:** 2 days

- **Dashboard**
  - Daily applications
  - Weekly applications
  - Interview rate
  - Rejection rate
  - Offer rate
  - Company statistics

---

### Sprint 10 — Production Readiness

**Duration:** 5 days

- **Security**
  - Secrets management
  - Rate limiting
  - Input validation
  - OAuth hardening
- **Database**
  - Alembic migrations
  - Index optimization
  - Connection pooling
- **Docker**
  - Backend container
  - PostgreSQL container
  - Docker Compose
- **Logging**
  - Structured logging
  - Request IDs
  - Error tracking
  - Pipeline logs
- **Monitoring**
  - Health endpoint
  - Metrics endpoint
  - Sync monitoring

---

### Sprint 11 — Frontend Integration

**Duration:** 4 days

- **Dashboard UI**
  - Login
  - Gmail connect
  - Sync progress
  - Applications view
  - Search & filters
  - Review queue
  - Analytics view

---

### Sprint 12 — Deployment

**Duration:** 3 days

- Environment configuration
- Production database setup
- Docker deployment
- AWS EC2 provisioning
- Nginx reverse proxy
- HTTPS & domain setup
- CI/CD pipeline

---

## 🚀 Stretch Goals (v2)

- Outlook integration
- Yahoo Mail integration
- Generic IMAP support
- Resume parsing
- Company enrichment
- Salary extraction
- AI‑generated email summaries
- Interview timeline view
- Calendar integration
- Browser extension
- Mobile application
- Multi‑user SaaS
- Team workspaces
- Notifications system
- LLM‑powered classification

---

## 📅 Estimated Timeline

| Sprint    | Focus                 | Duration |
| --------- | --------------------- | -------- |
| Sprint 0  | Architecture Planning | 1 day    |
| Sprint 1  | Email Pipeline        | 3–4 days |
| Sprint 2  | Gmail Infrastructure  | 3 days   |
| Sprint 3  | Database Redesign     | 2–3 days |
| Sprint 4  | Service Layer         | 2 days   |
| Sprint 5  | Repository Pattern    | 2 days   |
| Sprint 6  | Background Processing | 4 days   |
| Sprint 7  | Review Queue          | 3 days   |
| Sprint 8  | ML Improvements       | 4–5 days |
| Sprint 9  | Analytics Engine      | 2 days   |
| Sprint 10 | Production Readiness  | 5 days   |
| Sprint 11 | Frontend Integration  | 4 days   |
| Sprint 12 | Deployment            | 3 days   |

---

## 🎯 Final Deliverable

A production‑ready Email Intelligence Platform featuring:

- Hybrid **rules + ML** classification
- Robust Gmail synchronization
- Incremental email processing
- Human‑in‑the‑loop learning
- Modular pipeline architecture
- Repository & Service pattern
- Background job processing
- Analytics dashboard
- Production‑ready deployment
- Scalable architecture for future integrations
