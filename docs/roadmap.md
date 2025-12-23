# CamAtlas Roadmap

This roadmap outlines the planned phases and milestones for the CamAtlas project. 
It helps contributors understand the project goals, priorities, and workflow.

---

## Phase 1: Foundation 
- [x] Create GitHub repo
- [x] Add README.md
- [x] Add ethics.md (`docs/ethics.md`)
- [x] Add project logo (`assets/camatlas-logo.png`)
- [x] Create folder structure (`assets`, `crawler`, `data`, `backend`, `docs`)
- [x] Add LICENSE

---

## Phase 2: Seed Data & Basic Crawler
- [ ] Create `sources.json` with 100's known public webcam sites
- [ ] Write **first page scraper** (`crawler/page_scraper.py`) to fetch pages and extract embedded cameras
- [ ] Store camera metadata in **SQLite database** (`data/cameras.db`)
- [ ] Test with seed sources to confirm safe operation

---

## Phase 3: Index Expansion & Safe Discovery
- [ ] Add keyword-based discovery for **publicly listed webcams**
- [ ] Respect `robots.txt` and site rate limits
- [ ] Categorize feeds by type (traffic, tourism, wildlife) and country
- [ ] Add ability to remove cameras on owner request

---

## Phase 4: Backend / API 
- [ ] Build lightweight API using **FastAPI** or **Flask**
- [ ] Allow querying of the database: search by location, type, country
- [ ] Implement basic pagination

---

## Phase 5: Frontend / Visualization 
- [ ] Add map-based visualization (e.g., Leaflet.js or Google Maps)
- [ ] Display camera markers with clickable preview or link
- [ ] Integrate search/filter functionality

---

## Phase 6: Documentation & Community
- [ ] Complete `docs/roadmap.md` (this file)
- [ ] Add CONTRIBUTING.md and CODE_OF_CONDUCT.md
- [ ] Add example usage scripts (`scripts/run_crawler.py`)
- [ ] Add sample screenshots and demos in README

---

## Phase 7: Ongoing Maintenance
- [ ] Add new public webcams regularly
- [ ] Monitor for broken links and update database
- [ ] Accept pull requests safely and review for ethical compliance

---

Roadmap was sourced using ChatGPT
