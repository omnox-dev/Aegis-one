# AEGIS One: The Unified Digital Citadel

[![Status](https://img.shields.io/badge/Status-100%25%20Implemented-green)](https://github.com/KrackHack/AegisOne)
[![Theme](https://img.shields.io/badge/Theme-Snow%20Peak-blue)](https://aegis-one.vercel.app)

## 🏔️ Project Overview
**AEGIS One** is a high-performance, unified campus governance platform designed for the IIT Mandi community. Built to eliminate administrative fragmentation, AEGIS One (The Citadel) centralizes identity, academics, grievances, and campus life into a single, secure digital ecosystem.

The platform is architected around the **Seven Pillars Framework**, ensuring a harmonious balance between security, transparency, and master-level efficiency.

## 🏛️ The Seven Pillars (Feature List)

### PILLAR I: Identity & Governance
- **The Iron Gate:** Secure registration and login strictly for `@iitmandi.ac.in` emails.
- **High Command Dashboard:** Real-time analytics and user management for administrators.
- **Aegis Security:** Role-Based Access Control (RBAC) with bcrypt encryption and JWT security.

### PILLAR II: Voice (Grievance Management)
- **The Silent Scroll:** Anonymous/Identified submission with categorization and priority levels.
- **The Watcher's Eye:** Real-time status tracking (Submitted -> Under Review -> Resolved).
- **Evidence Vault:** Support for photo uploads and authority resolution remarks.

### PILLAR III: Fate (Academic Mastery)
- **The Destiny Manager:** Enrollment tracking and credit distribution calculator.
- **Attendance Logger:** Personal attendance tracking for scholars.
- **The Vault of Knowledge:** Searchabel database for PYQs and study materials.
- **Chronos Calendar:** Personalized academic deadlines and exam schedules.

### PILLAR IV: Opportunity (Internships & Tasks)
- **The Professor's Call:** Faculty portal for posting research/internship roles.
- **The Scholar's Ledger:** Personal academic task manager for milestone tracking.

### PILLAR V: The Commons (Life & Trade)
- **The Caravan Pool:** Peer-to-peer ride-sharing with a split-cost calculator.
- **The Mercenary Guild:** Campus freelancing marketplace for student skills.
- **Relic Recovery:** Image-based Lost & Found portal with claim verification.

### PILLAR VI: Connection (Community & Safety)
- **The Hall of Echoes:** Threaded discussion forum with upvote/downvote mechanics.
- **Pathfinder's Map:** Interactive campus grid with POI markers revealed on hover.
- **Guardian's Flare:** One-tap SOS system with automatic geolocation logging.

### PILLAR VII: The Spirit (Clubs & Announcements)
- **The Guild Halls:** Comprehensive club management and recruitment system.
- **The Universal Array:** Institue-wide announcement feed with priority pinning.

## 🛠️ Technology Stack
- **Frontend:** Next.js 15+, React 19, Tailwind CSS 4 (Snow Peak Design System).
- **Backend:** FastAPI (Python), SQLAlchemy ORM, Pydantic V2.
- **Database:** SQLite (for portability/demo) / PostgreSQL compatible.
- **Security:** JWT Authentication, Bcrypt password hashing.

## 🚀 Setup & Installation

### Prerequisites
- Node.js 20+
- Python 3.10+
- Pip (Python Package Manager)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database and seed initial data:
   ```bash
   python seed.py
   ```
4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 📉 Known Limitations & Future Scope
- **Limitations:** Currently uses SQLite for rapid demonstration; session persistence is limited to local storage.
- **Future Scope:** 
  - Integration with official Institute LDAP.
  - Native iOS/Android mobile applications.
  - AI-powered grievance auto-routing to specific departments.
  - Real-time bus tracking integration on the Pathfinder Map.

## 🤝 Contribution Guidelines
1. Fork the Repository.
2. Create a Feature Branch (`git checkout -b feature/citadel-pillar`).
3. Commit your changes.
4. Push to the Branch.
5. Open a Pull Request.

---
**Architected with ❤️ for IIT Mandi**
