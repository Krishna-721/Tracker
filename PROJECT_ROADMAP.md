# Tracker v2.0 Roadmap

## Vision

Build **Tracker** into a production‑ready Job Application Tracking Platform that automatically syncs Gmail, intelligently processes emails, tracks the full application lifecycle, and provides actionable insights through analytics.

---

## Current Progress

**Current Version:** v2.0

### Completed Features

- Gmail OAuth 2.0 Authentication
- Gmail Token Refresh
- Gmail Pagination
- Layered Backend Architecture
- Email Processing Pipeline
- Spam Filter
- Job Alert Filter
- Rule‑based Classification
- ML Fallback (TF‑IDF + Logistic Regression)
- Decision Engine
- Application Repository
- Application Service
- Application Matcher (Thread‑based)
- Async PostgreSQL
- Confidence Tracking
- Review Flag Support

---

### Sprint 1 – Backend Architecture ✅

**Status:** Completed

**Architecture**

- Layered Architecture
- Email Pipeline
- Pipeline Result Object
- Decision Engine
- Service Layer
- Repository Pattern
- Application Matcher
- Gmail Sync Refactor

**Pipeline Diagram**

```javascript
flowchart TD
    Gmail --> EmailParser --> SpamFilter --> JobAlertFilter --> RuleEngine --> MLClassifier --> DecisionEngine --> ApplicationService --> ApplicationRepository --> PostgreSQL
```

---

### Sprint 2 – Email Intelligence 🚧

**Status:** In Progress

**Focus:** Improve email understanding before storage.

#### 1. Email Parsing

- Improve HTML extraction
- Remove CSS, signatures, tracking pixels, unsubscribe sections
- Better plain‑text generation

#### 2. Email Type Detection

Detect whether an email is:

- Application
- Job Alert
- Newsletter
- Marketing
- Social
- Unknown

Only application‑related emails continue through the pipeline.

#### 3. Entity Extraction

**Company**: Stripe, Google, Amazon, Microsoft
**Role**: Software Engineer, Data Scientist, ML Engineer, Intern
**Recruiter**: John Doe
**Location**: Remote, Hyderabad, Bangalore

#### 4. Rule Engine Improvements

Expand rule coverage for stages such as:

- Application Received, Assessment, OA, Technical Round, HR Round, Interview, Offer, Rejection, Waitlist, Withdrawal

#### 5. Application Matching v2

- **Current**: Thread ID only
- **Future**: Multi‑field matching (Company, Role, Sender, Similarity Score)

---

### Sprint 3 – Application Lifecycle Tracking

**Core differentiator:** Full application timeline.

**Timeline Diagram**

```javascript
flowchart TD
    Applied --> Assessment --> Interview --> Offer --> Accepted
```

**Alternative outcome**

```javascript
flowchart TD
    Applied --> Rejected
```

**New Tables**

- `application_events` – stores every status transition
- `email_messages` – stores raw processed emails
- `sync_history` – tracks each Gmail sync

**Features**

- Timeline view
- Status history
- Last updated timestamp
- Duplicate detection
- Merge applications
- Event tracking

---

### Sprint 4 – Background Processing

**Goal:** Move synchronization to background jobs.

**Features**

- Incremental sync
- Background worker
- Retry failed emails
- Progress API
- Cancel sync
- Sync history

**Future Job Runners**: APScheduler, Celery, Redis Queue

---

### Sprint 5 – Human Review Queue

Create a feedback loop for model predictions.

**Review Dashboard**

- Needs review
- Approve prediction
- Correct prediction
- Manual status change

Corrections become future training data.

---

### Sprint 6 – ML Improvements

Replace synthetic bias with real‑world learning.

**Dataset**

- Collect real emails
- Human‑reviewed labels
- Remove synthetic bias

**Features**

- Subject weighting
- Sender weighting
- Better preprocessing
- HTML cleanup
- Signature removal

**Model Enhancements**

- Retrain Logistic Regression
- Cross‑validation
- Threshold optimization
- Probability calibration
- Evaluate need for transformer models

---

### Sprint 7 – Analytics Engine

Provide insights into job search progress.

**Dashboard Metrics**

- Total applications
- Active applications
- Interview rate
- Offer rate
- Rejection rate
- Company statistics
- Monthly & weekly trends
- Response time

---

### Sprint 8 – Production Readiness

Prepare backend for production deployment.

**Security**

- Secrets management
- OAuth hardening
- Input validation
- Rate limiting

**Database**

- Alembic migrations
- Index optimization
- Connection pooling

**Docker**

- Backend container
- PostgreSQL container
- Docker Compose setup

**Logging**

- Structured logs
- Request IDs
- Pipeline logs
- Error tracking

**Monitoring**

- Health endpoint
- Metrics endpoint
- Sync monitoring

---

### Sprint 9 – Frontend Integration

Build the complete Tracker UI.

**Dashboard UI Components**

- Gmail Connect
- Sync Progress
- Applications list
- Timeline view
- Search & filters
- Analytics charts
- Review Queue interface

---

### Sprint 10 – Deployment

Deploy Tracker to production environments.

**Steps**

- Set up CI/CD pipeline
- Configure cloud infrastructure (e.g., Azure/AWS)
- Enable autoscaling and load balancing
- Perform end‑to‑end smoke tests
- Monitor rollout and rollback if needed

---

### Sprint 8 – Production Readiness

Prepare backend for production.

#### Security

- Secrets management
- OAuth hardening
- Input validation
- Rate limiting

#### Database

- Alembic migrations
- Index optimization
- Connection pooling

#### Docker

- Backend container
- PostgreSQL container
- Docker Compose setup

#### Logging

- Structured logs
- Request IDs
- Pipeline logs
- Error tracking

#### Monitoring

- Health endpoint
- Metrics endpoint
- Sync monitoring

### Sprint 9 – Frontend Integration

Build the complete Tracker UI.

### Dashboard

\- Gmail Connect

\- Sync Progress

\- Applications

\- Timeline

\- Search

\- Filters

\- Analytics

\- Review Queue

\---

### Sprint 10 — Deployment

Deploy Tracker to production.

### Infrastructure

\- AWS EC2

\- PostgreSQL

\- Docker

\- Nginx

\- HTTPS

\- Domain Setup

#### CI/CD

\- GitHub Actions

\- Automated Deployment

\- Environment Configuration

\---

# Stretch Goals (v3)

### Email Providers

\- Outlook

\- Yahoo

\- Generic IMAP

### AI

\- AI Email Summaries

\- Company Enrichment

\- Salary Extraction

\- Resume Parsing

### Integrations

\- Google Calendar

\- Browser Extension

\- Notifications

\- Slack

\- Discord

### SaaS

\- Multi-user Support

\- Team Workspaces

\- Organization Dashboard

\---

# Estimated Timeline

\| Sprint | Focus | Duration |

\|---------|-------|----------|

\| Sprint 1 | Backend Architecture | ✅ Completed |

\| Sprint 2 | Email Intelligence | 5–7 days |

\| Sprint 3 | Application Lifecycle Tracking | 4–5 days |

\| Sprint 4 | Background Processing | 3–4 days |

\| Sprint 5 | Human Review Queue | 3 days |

\| Sprint 6 | ML Improvements | 5–7 days |

\| Sprint 7 | Analytics Engine | 3 days |

\| Sprint 8 | Production Readiness | 5 days |

\| Sprint 9 | Frontend Integration | 5–7 days |

\| Sprint 10 | Deployment | 3–4 days |

\---

# Final Deliverable

Tracker will evolve into a production-ready \*\*Job Application Intelligence Platform\*\* capable of:

\- Automatic Gmail synchronization

\- Intelligent email understanding

\- Hybrid Rules + ML classification

\- Application lifecycle tracking

\- Timeline-based status updates

\- Human-in-the-loop learning

\- Analytics dashboard

\- Scalable layered architecture

\- Production-ready deployment

\- Future multi-provider support
