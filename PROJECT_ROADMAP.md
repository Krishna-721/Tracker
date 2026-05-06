# Project Roadmap: Job Application Tracker

## Vision
Transform the project from a passive "Email Logger" into an active "Career CRM" that tracks the lifecycle of job applications, providing a unified dashboard and a unique "Ghosting Tab" to identify non-responsive companies.

## Current State (The "Engine")
- [x] Gmail OAuth2 Integration
- [x] ML-based Email Classification (TF-IDF + Logistic Regression)
- [x] Async FastAPI Backend & PostgreSQL Storage
- [x] Basic Analytics API

## The "Base-First" Strategy
Before building the UI, the foundation must move from tracking **Emails** to tracking **Application Entities**.

### Phase 1: Hardening the Base (Current Focus)
- [ ] **Thread-to-Application Mapping:** Transition from creating a row per email to updating a single application record based on `gmail_thread_id`.
- [ ] **Structured Extraction:** Implement NER or LLM-based extraction to populate `company` and `role` fields automatically.
- [ ] **Timestamp Engine:** Ensure rigorous tracking of `updated_at` to enable time-based state changes.

### Phase 2: The "Skills" Layer
- [ ] **The Ghosting Engine:** Implement a background service that moves applications to the "Ghosted" state if no contact has occurred within X days.
- [ ] **State Machine:** Define clear transitions (Applied $\rightarrow$ Interview $\rightarrow$ Offer/Rejected/Ghosted).
- [ ] **Advanced Analytics:** Calculate conversion rates and average response times.

### Phase 3: The "Looks" (Frontend)
- [ ] **Kanban Dashboard:** A drag-and-drop interface for managing application stages.
- [ ] **Ghosting Tab:** A dedicated view for companies that have gone silent.
- [ ] **Analytics Visualization:** Charts showing the application funnel.

## Key Feature: The Ghosting Tab
- **Purpose:** Identify companies that have not responded within a specific timeframe (e.g., 14 days).
- **Technical Requirement:** Requires a background cron job checking `updated_at` against the current date.
