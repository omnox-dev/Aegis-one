# AEGIS One - comprehensive University Management System

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📖 Overview

**AEGIS One** is a modern, unified platform designed to streamline university operations and enhance campus life. It integrates academic management, grievance redressal, club activities, internship opportunities, and community engagement into a single, intuitive interface.

### Key Features

*   **User Management**: Role-based access control (Student, Faculty, Admin).
*   **Grievance Redressal**: Secure and transparent process for submitting and tracking complaints.
*   **Academic Hub**: Centralized access to course materials, attendance records, and announcements.
*   **Club & Event Management**: Discover and join clubs, view upcoming events, and manage memberships.
*   **Career Opportunities**: Internship listings and application tracking.
*   **Community Forum**: Discussion boards for academic and social interaction.
*   **Emergency Response**: Integrated SOS feature for campus safety.

## 🏗️ Architecture

The system is built on a robust, scalable architecture:

*   **Frontend**: [Next.js](https://nextjs.org/) (React) for a responsive and dynamic user experience.
*   **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python) for high-performance API services.
*   **Database**: [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) ORM for reliable data management.
*   **Authentication**: JWT-based secure authentication flow.

![Architecture Diagram](https://mermaid.ink/img/pako:eNqNkk1vwjAMhv9K5HMHpB04dUICTmjHbdMOvVylNImpE0eOE6iq_vc5LWWlHThFidx_7dh-k_VOWS0M2Xfa3rB2yNoJ2wrbSttI20zbTttB21HbSdtJ203bQxun7aTto-2nHaAdph2kHaYdph2lHa0dpR2jnaAdpx2nvaddpL2nvddyR0uXlt5K6Z2U3kvpvZTeS-m9lD5I6YOUPljdsTpaHbE6UnW0OlJ1tDpSdbQ6UnW0OlJ1tDpSdbQ6UnW0OlJ1tHpS9aTqSdWTqidVT6qeVD2pelL1pOpJ1ZOqJ1VPqp5UPal6UvWk6knVk6onVU-qvqX6lupbqm-pvqX6lupbqm-pvqX6lupbqm-pvqX6lupbqm-pvqX6lupbqm-pvqX6lupbqm-pvqX6lupbqm-pvqX6lupbqu-ovqP6juo7qu-ovqP6juo7qu-ovqP6juo7qu-ovqP6juo7qu-ovqP6juo7qu-ovqP6juo7qu-ovqP6juo7qu-ovqP6jup7qu-pvqf6nup7qu-pvqf6nup7qu-pvqf6nup7qu-pvqf6nup7qu-pvqf6nup7qu-pvqf6nup7qu-pvqf6nup7qu-pvqf6nup76u-pv6f-nvp76u-pv6f-nvp76u-pv6f-nvp76u-pv6f-nvp76u-pv6f-nvp76u-pv6f-nvp76u-pv6f-nvp76u-pv6f-nvp76u-pv6f-nvp76u-pv6f-nvp76u-pv6f-nvp76u-pv6f)

## 📂 Project Structure

```bash
.
├── backend/                # FastAPI Backend Application
│   ├── app/
│   │   ├── api/            # API Route Handlers
│   │   ├── core/           # Configuration & Security
│   │   ├── models/         # SQLAlchemy Database Models
│   │   ├── schemas/        # Pydantic Schemas
│   │   └── services/       # Business Logic Layer
│   ├── requirements.txt    # Python Dependencies
│   └── seed.py             # Database Seeding Script
├── frontend/               # Next.js Frontend Application
│   ├── src/
│   │   ├── app/            # App Router Pages
│   │   ├── components/     # Reusable React Components
│   │   └── lib/            # Utilities & Helpers
│   ├── public/             # Static Assets
│   └── package.json        # Node.js Dependencies
└── README.md               # Project Documentation
```

## 🛠️ Tech Stack

### Backend
-   **Framework**: FastAPI
-   **Language**: Python 3.10+
-   **Database**: PostgreSQL / SQLite (Development)
-   **ORM**: SQLAlchemy + Alembic (Migrations)
-   **Auth**: OAuth2 with JWT (JSON Web Tokens)

### Frontend
-   **Framework**: Next.js 14 (App Directory)
-   **Language**: TypeScript
-   **Styling**: Tailwind CSS
-   **State Management**: React Context / Hooks
-   **HTTP Client**: Axios

## 🚀 Getting Started

Follow these instructions to set up the project locally.

### Prerequisites
-   [Python 3.10+](https://www.python.org/)
-   [Node.js 18+](https://nodejs.org/)
-   [PostgreSQL](https://www.postgresql.org/) (Optional for dev, SQLite supported)

### Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Create a virtual environment:
    ```bash
    python -m venv venv
    On Windows: venv\Scripts\activate
    On Linux/Mac: source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Configure Environment Variables:
    Create a `.env` file in `backend/` based on `config.py` defaults or the example provided.
    ```env
    DATABASE_URL=sqlite:///./aegis_one.db
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ```

5.  Run Database Migrations (if applicable) or Initialize DB:
    ```bash
    # If using alembic
    alembic upgrade head
    ```

6.  Start the Development Server:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`. Documentation at `/docs`.

### Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```

3.  Configure Environment Variables:
    Create a `.env.local` file in `frontend/`:
    ```env
    NEXT_PUBLIC_API_URL=http://localhost:8000
    ```

4.  Start the Development Server:
    ```bash
    npm run dev
    ```
    The application will be running at `http://localhost:3000`.

## 🗄️ Database Schema

The database is designed with the following core entities:

### Users & Roles
*   **User**: Stores authentication details, role (`student`, `faculty`, `admin`), and profile info.

### Academic Modules
*   **Course**: Information about subjects, credits, and instructors.
*   **Enrollment**: Links students to courses.
*   **Attendance**: Tracks student attendance per course.
*   **Resource**: Academic materials (notes, PYQs) uploaded by faculty/students.

### Campus Life
*   **Club**: Student organizations and their details.
*   **ClubMember**: Manages club memberships and roles.
*   **ClubEvent**: Events organized by clubs.
*   **LostFoundItem**: Repository for reported lost and found items.

### Administration & Support
*   **Grievance**: Complaints filed by students, tracked by status (`pending`, `resolved`).
*   **Internship**: Career opportunities posted for students.
*   **Incident**: Emergency reports linked to locations.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest improvements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
