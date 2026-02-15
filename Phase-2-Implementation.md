# AEGIS Platform — Phase 2 Implementation Plan

> **Generated**: 14 Feb 2026 · **Stack**: Next.js 15 (App Router) + FastAPI + SQLite  
> **Goal**: Complete all 4 mandatory pillars to production quality, then add maximum bonus pillars for hackathon differentiation.

---

## Current State Audit (What Exists Today)

### ✅ DONE
| Feature | Backend | Frontend |
|---|---|---|
| Role-based auth (Student/Faculty/Authority/Admin) | ✅ JWT + bcrypt | ✅ Login/Register/Context |
| User CRUD (admin) | ✅ GET/PATCH/DELETE | ✅ Full management UI |
| Grievance CRUD + comments | ✅ Full REST API | ✅ List/Detail/Submit/Comment |
| Grievance status tracking | ✅ Status update API | ✅ Inline dropdowns for admin |
| Course listing + enrollment | ✅ Create/List/Enroll | ✅ Card UI + Enroll button |
| Internship listing + apply | ✅ Create/List/Apply | ✅ Card UI + Apply button |
| Dashboard stats (role-aware) | ✅ /api/dashboard/stats | ✅ All 4 role dashboards |
| Profile page | — | ✅ View/Edit form (save not wired) |

### ❌ MISSING (Required by Master Plan)
| Requirement | Pillar | Status |
|---|---|---|
| Institute email restriction | I | ❌ Not enforced |
| Anonymous grievance submission | II | ❌ Not implemented |
| Location tagging on grievances | II | ❌ Missing field |
| Photo upload on grievances | II | ❌ No file upload |
| Grievance assign to authority | II | ❌ UI missing |
| Urgent priority level | II | ❌ Only low/medium/high |
| Credit calculator | III | ❌ Not built |
| Attendance logger | III | ❌ Not built |
| Resource repository (PYQs) | III | ❌ Not built |
| Academic calendar | III | ❌ Not built |
| Application status tracking (shortlisted/accepted/rejected) | IV | ❌ Basic only |
| Faculty application management (accept/reject/shortlist) | IV | ❌ Not built |
| Personal task manager (Scholar's Ledger) | IV | ❌ Not built |
| Required skills on internships | IV | ❌ Missing field |
| Duration field on internships | IV | ❌ Missing field |
| Activity logs / audit trails | I | ❌ Not built |
| Announcement system | VII | ❌ Not built |
| Lost & Found | V | ❌ Not built |

---

## Build Order & Priority

### 🔴 CRITICAL (Mandatory Pillar Gaps — Do These First)

#### Phase 2A: Pillar I Hardening (Identity & Governance) — ~30 min
1. **Institute email restriction** — Backend: validate `@iitmandi.ac.in` on register  
2. **Admin activity logs** — New `AuditLog` model, log all admin actions  
3. **System health monitoring** — Backend: `/api/admin/system-stats` endpoint  
4. **Admin analytics page** — Frontend: platform-wide analytics dashboard  

#### Phase 2B: Pillar II Completion (Grievance System) — ~45 min
5. **Add `location` field** — Backend model + schema + frontend form  
6. **Add `urgent` priority** — Extend priority enum everywhere  
7. **Anonymous submission** — `is_anonymous` boolean on grievances  
8. **Photo upload** — Backend file upload endpoint + frontend dropzone  
9. **Authority assignment UI** — Admin can assign grievance to a user  
10. **Resolution remarks** — Required remarks when status changes  

#### Phase 2C: Pillar III — Academic Mastery (NEW) — ~60 min
11. **Course credits** — Add `credits` + `course_type` fields to Course model  
12. **Credit calculator page** — Frontend: show total/major/minor/elective breakdown  
13. **Attendance model** — New `Attendance` model (student, course, date, present)  
14. **Attendance logger page** — Frontend: mark/view attendance per course  
15. **Resource model** — New `Resource` model (title, file_url, course_code, year, exam_type, tags)  
16. **Resource repository page** — Frontend: browse/upload/search PYQs + notes  
17. **Academic calendar model** — New `AcademicEvent` model  
18. **Academic calendar page** — Frontend: calendar view with personal reminders  

#### Phase 2D: Pillar IV Completion (Opportunities & Tasks) — ~45 min
19. **Expand Internship fields** — Add `required_skills`, `duration` to model  
20. **Application status flow** — Extend from `applied` → `submitted/under_review/shortlisted/accepted/rejected`  
21. **Faculty application management** — UI for faculty to review/accept/reject  
22. **Task model** — New `Task` model (title, description, due_date, category, status, user_id)  
23. **Scholar's Ledger page** — Frontend: personal task manager with categories + progress  

### 🟡 HIGH IMPACT BONUS — Do These for Maximum Points

#### Phase 2E: Pillar V — The Commons (Bonus) — ~40 min  
24. **Lost & Found model** — `LostFoundItem` (title, description, image, location, category, status, posted_by)  
25. **Lost & Found pages** — Browse/post items, claim system  

#### Phase 2F: Pillar VII — Announcements (Bonus) — ~30 min
26. **Announcement model** — `Announcement` (title, content, category, posted_by, pinned)  
27. **Announcements page** — Feed with category filter, admin can create/pin  

#### Phase 2G: Pillar VI — Community & Safety (Bonus) — ~40 min
28. **Discussion forum model** — `ForumPost`, `ForumComment` with votes  
29. **Forum pages** — Reddit-style threaded view, upvote/downvote  
30. **Emergency SOS** — One-tap button with geolocation + incident logging  

---

## Detailed Implementation Specs

### New Backend Models Required

```python
# models/attendance.py
class Attendance(Base):
    __tablename__ = "attendance"
    id, student_id (FK users), course_id (FK courses),
    date (Date), status (present/absent/late),
    created_at

# models/resource.py
class Resource(Base):
    __tablename__ = "resources"
    id, title, file_url, course_code, year, exam_type,
    tags (Text/JSON), uploaded_by (FK users),
    created_at

# models/academic_event.py
class AcademicEvent(Base):
    __tablename__ = "academic_events"
    id, title, description, event_date, event_type
    (exam/assignment/holiday/deadline),
    course_id (FK courses, nullable), created_by (FK users),
    created_at

# models/task.py
class Task(Base):
    __tablename__ = "tasks"
    id, title, description, due_date, category
    (assignment/project/personal/exam_prep),
    status (todo/in_progress/done), priority,
    user_id (FK users), created_at

# models/lost_found.py
class LostFoundItem(Base):
    __tablename__ = "lost_found_items"
    id, title, description, image_url, location,
    category (electronics/books/id_cards/clothing/other),
    item_type (lost/found), status (open/claimed/closed),
    posted_by (FK users), claimed_by (FK users, nullable),
    created_at

# models/announcement.py
class Announcement(Base):
    __tablename__ = "announcements"
    id, title, content, category
    (academic/events/administrative/emergency),
    pinned (bool), posted_by (FK users),
    created_at

# models/forum.py
class ForumPost(Base):
    __tablename__ = "forum_posts"
    id, title, content, category
    (academics/campus_life/events/tech_support/general),
    author_id (FK users), upvotes, downvotes,
    created_at

class ForumComment(Base):
    __tablename__ = "forum_comments"
    id, post_id (FK forum_posts), parent_id (FK self, nullable),
    author_id (FK users), content,
    upvotes, downvotes, created_at

# models/audit_log.py
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id, user_id (FK users), action, target_type,
    target_id, details (Text/JSON), created_at
```

### New Backend API Routers Required

| Router | Endpoints |
|---|---|
| `attendance.py` | `POST /mark`, `GET /course/{id}`, `GET /my-attendance` |
| `resources.py` | `GET /`, `POST /upload`, `GET /{id}`, `DELETE /{id}` |
| `calendar.py` | `GET /events`, `POST /events`, `GET /my-events` |
| `tasks.py` | `GET /`, `POST /`, `PATCH /{id}`, `DELETE /{id}` |
| `lost_found.py` | `GET /`, `POST /`, `PATCH /{id}/claim`, `DELETE /{id}` |
| `announcements.py` | `GET /`, `POST /`, `DELETE /{id}` |
| `forum.py` | `GET /posts`, `POST /posts`, `GET /posts/{id}`, `POST /posts/{id}/comments`, `POST /posts/{id}/vote` |
| `audit.py` | `GET /logs` (admin only) |

### New Frontend Pages Required

| Route | Purpose |
|---|---|
| `/dashboard/academics` | Credit calculator + course overview |
| `/dashboard/attendance` | Mark + view attendance |
| `/dashboard/resources` | PYQ / study material repository |
| `/dashboard/calendar` | Academic calendar with events |
| `/dashboard/tasks` | Scholar's Ledger (personal task manager) |
| `/dashboard/lost-found` | Lost & Found portal |
| `/dashboard/announcements` | Campus announcements feed |
| `/dashboard/forum` | Discussion forum |
| `/dashboard/analytics` | Admin analytics + audit logs |

### Sidebar Navigation Update

```
STUDENT sees:
  Dashboard | Grievances | Courses | Academics | Attendance | 
  Resources | Calendar | Tasks | Internships | Lost & Found |
  Forum | Announcements

FACULTY sees:
  Dashboard | Grievances | Courses | Internships | Resources |
  Calendar | Announcements | Forum

AUTHORITY sees:
  Dashboard | Grievances | Users | Announcements | Analytics

ADMIN sees:
  All of the above
```

---

## Grievance Model Updates

```python
# Add to Grievance model:
location: Mapped[str | None]  # campus location
is_anonymous: Mapped[bool] = mapped_column(default=False)

# Add to GrievanceCreate schema:
location: str | None = None
is_anonymous: bool = False

# Add "urgent" to priority options everywhere
```

## Course Model Updates

```python
# Add to Course model:
credits: Mapped[int] = mapped_column(Integer, default=3)
course_type: Mapped[str] = mapped_column(String(20), default="major")
# course_type: major, minor, elective, lab, project
```

## Internship Model Updates

```python
# Add to Internship model:
required_skills: Mapped[str | None]  # comma-separated
duration: Mapped[str | None]  # e.g. "3 months"

# Update Application status options:
# applied → submitted, under_review, shortlisted, accepted, rejected
```

---

## Execution Order (Recommended)

| Step | What | Time Est. |
|---|---|---|
| 1 | Grievance model/schema updates (location, anonymous, urgent) | 10 min |
| 2 | Course model updates (credits, course_type) | 5 min |
| 3 | Internship model updates (required_skills, duration, status flow) | 10 min |
| 4 | Institute email validation on backend | 5 min |
| 5 | New models: Attendance, Resource, AcademicEvent, Task, AuditLog | 15 min |
| 6 | New models: LostFoundItem, Announcement, ForumPost/Comment | 10 min |
| 7 | New API routers for all new models | 30 min |
| 8 | Register new routers in main.py | 5 min |
| 9 | Update api.ts with all new endpoints + types | 15 min |
| 10 | Build new frontend pages (Academics, Attendance, Resources, Calendar, Tasks) | 40 min |
| 11 | Build bonus pages (Lost & Found, Announcements, Forum) | 30 min |
| 12 | Update sidebar navigation for all roles | 10 min |
| 13 | Admin analytics page with audit logs | 15 min |
| 14 | Update submit grievance form (location, anonymous, urgent) | 10 min |
| 15 | Faculty application management UI | 15 min |
| 16 | Enhanced seed data for demo | 15 min |
| 17 | Final UI polish + responsive testing | 15 min |
| **TOTAL** | | **~4 hours** |

---

## File Structure After Phase 2

```
backend/app/
├── api/
│   ├── auth.py          ← (update: email validation)
│   ├── grievances.py    ← (update: location, anonymous, assign)
│   ├── courses.py       ← (update: credits)
│   ├── internships.py   ← (update: skills, duration, status)
│   ├── users.py
│   ├── dashboard.py     ← (update: new stats)
│   ├── attendance.py    ← NEW
│   ├── resources.py     ← NEW
│   ├── calendar.py      ← NEW
│   ├── tasks.py         ← NEW
│   ├── lost_found.py    ← NEW
│   ├── announcements.py ← NEW
│   ├── forum.py         ← NEW
│   └── audit.py         ← NEW
├── models/
│   ├── user.py
│   ├── grievance.py     ← (update)
│   ├── course.py        ← (update)
│   ├── internship.py    ← (update)
│   ├── attendance.py    ← NEW
│   ├── resource.py      ← NEW
│   ├── academic_event.py← NEW
│   ├── task.py          ← NEW
│   ├── lost_found.py    ← NEW
│   ├── announcement.py  ← NEW
│   ├── forum.py         ← NEW
│   └── audit_log.py     ← NEW
├── schemas/
│   ├── (matching schema for each new model)
│   └── ...
└── main.py              ← (register new routers)

frontend/src/app/dashboard/
├── page.tsx
├── layout.tsx           ← (update sidebar nav)
├── grievances/          ← (update form: location, anon, urgent)
├── courses/
├── internships/
├── users/
├── profile/
├── academics/           ← NEW (credit calculator)
├── attendance/          ← NEW
├── resources/           ← NEW
├── calendar/            ← NEW
├── tasks/               ← NEW
├── lost-found/          ← NEW
├── announcements/       ← NEW
├── forum/               ← NEW
└── analytics/           ← NEW
```

---

## Key Design Decisions

1. **IIT Mandi Theme**: Sky blues (#3B82F6), forest greens (#22C55E), snow whites, slate grays — already partially in place
2. **Mobile-First**: All new pages must be fully responsive
3. **SQLite**: Keep for hackathon — simple, portable, zero-config
4. **File uploads**: Use local `/uploads/` directory for hackathon (images, PYQs)
5. **Seed data**: Comprehensive demo data for all 4 roles showing every feature

---

## Success Metrics (Hackathon Scoring)

| Criterion | Weight | Our Target |
|---|---|---|
| Architectural Integrity | 20% | Clean code, documented schema, RBAC, bcrypt, JWT |
| Pillar Completeness | 40% | All 4 core pillars + 3 bonus pillars fully functional |
| UX / UI Quality | 25% | Premium design, role-based navigation, responsive, accessible |
| Innovation | 15% | Forum, SOS, audit logs, analytics, auto-alerts |

**Let's build. 🏗️**
