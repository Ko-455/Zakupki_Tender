# Tender Analyzer 🏗️

A platform for monitoring Russian government procurement (zakupki.gov.ru) and generating quick bids for construction supplies.

## Features
- **AI Scraper**: Powered by `scrapegraph-ai` & Google Gemini.
- **Smart Quote**: Matches tender requirements with internal product database.
- **Telegram Bot**: Instant notifications about new tenders.
- **FastAPI**: Robust backend with JWT auth.

## Quick Start (Docker)
1. Rename `.env.example` to `.env` and configure keys.
2. Run:
   ```bash
   docker-compose up --build
   ```
3. API available at `http://localhost:8000/docs`.

---
