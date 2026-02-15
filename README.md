# AEGIS One - Comprehensive University Management System

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📖 Overview & Problem Context

**The Problem:**
University campuses are complex ecosystems where students juggle academics, social life, career building, and administrative hurdles. Currently, these functions are fragmented across disjointed portals—one for grades, another for complaints, WhatsApp for clubs, and bulletin boards for lost items. This fragmentation leads to:
*   Missed deadlines and opportunities.
*   Lack of transparency in grievance redness.
*   Inefficient resource sharing (travel, skills).
*   Safety concerns due to delayed emergency reporting.

**Our Solution: AEGIS One**
AEGIS One is a unified digital campus architecture. It consolidates every aspect of university life—from checking attendance to booking a carpool—into a single, cohesive, and modern interface. We aim to bridge the gap between administration and students, fostering a transparent, efficient, and connected campus community.

## ✨ Complete Feature List

### 🏛️ Core Pillars (Essential Modules)
1.  **Academic Hub**:
    *   **Course Management**: View enrolled courses, syllabus, and faculty details.
    *   **Attendance Tracking**: Real-time attendance percentage and history.
    *   **Resource Repository**: Centralized upload/download for notes and PYQs.
2.  **Grievance Redressal System**:
    *   **Transparent Tracking**: File complaints (Hostel/Academic) and track status (Pending -> Resolved).
    *   **Priority Levels**: Urgent flagging for critical issues.
3.  **Campus Life & Clubs**:
    *   **Club Discovery**: Browse and join technical, cultural, or sports clubs.
    *   **Event Calendar**: Unified schedule for all club activities and deadlines.
4.  **User Roles & Security**:
    *   **Role-Based Access**: Distinct dashboards for Students, Faculty, and Admins.
    *   **Secure Auth**: JWT-based authentication and session management.

### 🚀 Bonus Pillars (Advanced Implementations)
1.  **Caravan (Smart Carpooling)**:
    *   Students can pool cab rides to nearby cities, splitting costs and reducing carbon footprint.
2.  **Mercenary (Student Gig Economy)**:
    *   A peer-to-peer marketplace where students offer skills (tutoring, design, coding) for gigs/bounties.
3.  **SOS / Emergency Response**:
    *   One-tap emergency trigger sharing live location with campus security authorities.
4.  **Lost & Found**:
    *   Digital board to report lost items or claim found ones with image support.
5.  **Community Forum**:
    *   Reddit-style discussion threads for doubts, discussions, and polls.

## 🛠️ Technology Stack & Justification

| Component | Technology | Justification |
| :--- | :--- | :--- |
| **Frontend** | **Next.js 14** (React) | Provides server-side rendering for performance, excellent SEO, and a modern App Router for intuitive navigation. |
| **Styling** | **Tailwind CSS** | rapid UI development with a consistent, utility-first design system ensuring mobile responsiveness. |
| **Backend** | **FastAPI** (Python) | High-performance (async/await), automatic Swagger documentation help, and easy integration with Python AI/Data libraries. |
| **Database** | **PostgreSQL** | Robust relational database perfect for complex relationships between students, courses, and events. |
| **ORM** | **SQLAlchemy** | Ensures type-safe database interactions and easy schema migrations. |
| **Auth** | **JWT + OAuth2** | Stateless, secure, and scalable authentication standard. |

## 📸 Screenshots & Demos

*(Add your screenshots in the `screenshots/` folder and link them here)*

| **Student Dashboard** | **Grievance Portal** |
| :---: | :---: |
| ![Student Dashboard](screenshots/dashboard_student.png) | ![Grievance Portal](screenshots/grievance_portal.png) |

| **Club Events** | **Dark Mode** |
| :---: | :---: |
| ![Club Events](screenshots/club_events.png) | ![Dark Mode](screenshots/dark_mode.png) |

## 🚀 Setup & Installation Guide

Follow these steps to deploy AEGIS One locally.

### Prerequisites
*   Git
*   Python 3.10+
*   Node.js 18+ & npm/yarn
*   PostgreSQL Service (running locally or via Docker)

### Step 1: Clone the Repository
```bash
git clone https://github.com/omnox-dev/Aegis-one.git
cd Aegis-one
```

### Step 2: Backend Setup
```bash
cd backend

# Create Virtual Environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Configure Environment
# Create a .env file and add:
# DATABASE_URL=postgresql://user:password@localhost/aegis_db
# SECRET_KEY=your_secure_secret

# Run Migrations
alembic upgrade head

# Start Server
uvicorn app.main:app --reload
```
*Backend is now running at `http://localhost:8000`*

### Step 3: Frontend Setup
```bash
cd ../frontend

# Install Dependencies
npm install

# Configure Environment
# Create .env.local and add:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start App
npm run dev
```
*Frontend is now running at `http://localhost:3000`*

## 🚧 Known Limitations & Future Scope

### Limitations
*   **Payment Integration**: The 'Mercenary' gig payments are currently manual/cash-based; no integrated payment gateway yet.
*   **Real-time Chat**: Messaging is REST-based; WebSocket integration needed for instant chat.

### Future Roadmap
*   **AI-Powered Insights**: Suggesting clubs/internships based on student academic performance.
*   **Mobile App**: Building a React Native version for better on-the-go access.
*   **Blockchain Verification**: Storing certificates and internship completion records on-chain.

## 🤝 Contributing
Refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License
MIT License.
