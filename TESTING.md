# AEGIS One — Phase 2 Complete Testing Guide

> **Last updated:** 2026-02-14  
> Follow each section top-to-bottom. Every checkbox is one testable action.  
> Password for **all** seeded accounts: `password123`

---

## 0 — Prerequisites

- [ ] Backend running on `http://127.0.0.1:8000`
  ```powershell
  cd backend
  .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
  ```
- [ ] Frontend running on `http://localhost:3000`
  ```powershell
  cd frontend
  npm run dev
  ```
- [ ] Database seeded (run once, clears old data)
  ```powershell
  cd backend
  .\venv\Scripts\python.exe seed.py
  ```
- [ ] Open `http://localhost:3000` in your browser — you should see the landing / login page.

---

## 1 — Authentication (All Roles)

### 1.1 Student Login
- [ ] Go to `http://localhost:3000/login`
- [ ] Enter email: `student1@iitmandi.ac.in`, password: `password123`
- [ ] Click **Login**
- [ ] ✅ Redirected to `/dashboard`
- [ ] ✅ Sidebar shows: Dashboard, Announcements, Grievances, Submit Grievance, Courses, Attendance, Resources, Calendar, Tasks, Internships, Lost & Found, Forum, Profile
- [ ] ✅ Bottom-left shows name **Aarav Patel** and role **student**
- [ ] Click **Logout** (bottom-left icon) → redirected to login

### 1.2 Faculty Login
- [ ] Login as `faculty1@iitmandi.ac.in` / `password123`
- [ ] ✅ Dashboard loads
- [ ] ✅ Sidebar shows: Dashboard, Announcements, Grievances, Courses, Calendar, Resources, Internships, Forum, Profile

### 1.3 Authority Login
- [ ] Login as `authority@iitmandi.ac.in` / `password123`
- [ ] ✅ Dashboard loads
- [ ] ✅ Sidebar shows: Dashboard, Announcements, Grievances, Users, Calendar, Lost & Found, Forum, Profile

### 1.4 Admin Login
- [ ] Login as `admin@iitmandi.ac.in` / `password123`
- [ ] ✅ Dashboard loads
- [ ] ✅ Sidebar shows: Dashboard, Announcements, Grievances, Users, Courses, Calendar, Internships, Resources, Lost & Found, Forum, Profile

---

## 2 — Dashboard (Pillar I)

> Login as **student1@iitmandi.ac.in**

- [ ] Navigate to **Dashboard** (sidebar)
- [ ] ✅ Stats cards display (total grievances, courses enrolled, etc.)
- [ ] ✅ No errors in browser console

> Login as **admin@iitmandi.ac.in**

- [ ] Navigate to **Dashboard**
- [ ] ✅ Admin-specific stats display (total users, total grievances, etc.)

---

## 3 — Announcements (Pillar VII — Universal Array)

### 3.1 View Announcements (Student)
> Login as **student1@iitmandi.ac.in**

- [ ] Click **Announcements** in sidebar
- [ ] ✅ Page title: "Announcements"
- [ ] ✅ 5 seeded announcements visible
- [ ] ✅ Pinned announcements (📌) appear at top: "Mid-Semester Exam Schedule Released" and "Emergency: Water Supply Disruption"
- [ ] ✅ Each announcement shows: title, content, category badge, author name, date
- [ ] ✅ Category badges have distinct colors (academic=blue, events=purple, emergency=red, etc.)

### 3.2 Filter Announcements
- [ ] Click **academic** filter pill → only academic announcements shown
- [ ] Click **emergency** filter pill → only emergency announcements shown
- [ ] Click **All** pill → all announcements shown again

### 3.3 Student Cannot Create
- [ ] ✅ "New Announcement" button is **NOT** visible (students can't post)

### 3.4 Create Announcement (Admin)
> Login as **admin@iitmandi.ac.in**

- [ ] Click **Announcements** → Click **New Announcement** button
- [ ] ✅ Form appears with Title, Content, Category dropdown, Pin checkbox
- [ ] Fill in:
  - Title: `Test Announcement from Admin`
  - Content: `This is a test announcement to verify the feature works correctly.`
  - Category: `general`
  - Pin: ✅ checked
- [ ] Click **Post**
- [ ] ✅ Form closes, new announcement appears at top (pinned)

### 3.5 Delete Announcement (Admin)
- [ ] Find the test announcement just created
- [ ] Click the 🗑️ delete icon
- [ ] Confirm the deletion dialog
- [ ] ✅ Announcement removed from the list

---

## 4 — Grievances (Pillar II — The Sentinel's Watch)

### 4.1 View Grievances (Student)
> Login as **student1@iitmandi.ac.in**

- [ ] Click **Grievances** in sidebar
- [ ] ✅ List of grievances visible (student sees only their own)
- [ ] ✅ Each grievance shows: title, category, priority, status badge
- [ ] ✅ Status filters work (pending, in_review, in_progress, resolved)

### 4.2 Submit a New Grievance
- [ ] Click **Submit Grievance** in sidebar
- [ ] Fill in:
  - Category: `infrastructure`
  - Title: `Broken street light near hostel gate`
  - Description: `The street light near the main hostel gate has been broken for a week. It is very dark and unsafe at night.`
  - Priority: `high`
  - Location: `Hostel Main Gate`
  - Anonymous: ❌ unchecked
- [ ] Click **Submit**
- [ ] ✅ Redirected to grievances list, new grievance appears

### 4.3 Submit Anonymous Grievance
- [ ] Click **Submit Grievance** again
- [ ] Fill in:
  - Category: `food`
  - Title: `Hygiene issue in South Mess`
  - Description: `Found insects in the food served during dinner.`
  - Anonymous: ✅ checked
- [ ] Click **Submit**
- [ ] ✅ Grievance appears in list

### 4.4 View Grievance Detail
- [ ] Click on any grievance from the list
- [ ] ✅ Detail page shows: title, description, category, priority, status, location, timestamps
- [ ] ✅ Comments section visible at the bottom

### 4.5 Add Comment
- [ ] On the grievance detail page, type a comment: `Any update on this issue?`
- [ ] Click **Submit** / press Enter
- [ ] ✅ Comment appears in the comments section

### 4.6 Authority Manages Grievances
> Login as **authority@iitmandi.ac.in**

- [ ] Click **Grievances**
- [ ] ✅ All grievances visible (not just own)
- [ ] Click on "Wi-Fi connectivity issues in Hostel Block C"
- [ ] ✅ Detail page loads with comments from seed data
- [ ] Change status to `in_progress` or `resolved`
- [ ] ✅ Status updates successfully

---

## 5 — Courses & Credit Calculator (Pillar III)

### 5.1 View Courses (Student)
> Login as **student1@iitmandi.ac.in**

- [ ] Click **Courses** in sidebar
- [ ] ✅ 6 seeded courses visible
- [ ] ✅ Each course shows: name, code, description, semester, credits, course type, faculty name
- [ ] ✅ Courses the student is enrolled in are marked

### 5.2 Enroll in a Course
- [ ] Find a course the student is NOT enrolled in (e.g. "Technical Writing - HS101")
- [ ] Click **Enroll** button
- [ ] ✅ Button changes to "Enrolled" or similar indicator
- [ ] ✅ Enrollment count increases

### 5.3 View My Enrollments
- [ ] Check enrolled courses section / tab
- [ ] ✅ Shows enrolled courses with credits and course type
- [ ] ✅ Credit total is displayable (4+4+3+1 = 12 from seed for student1, plus any new enrollments)

### 5.4 Faculty Creates a Course
> Login as **faculty1@iitmandi.ac.in**

- [ ] Click **Courses**
- [ ] Click **Create Course** (or equivalent button)
- [ ] Fill in:
  - Name: `Cloud Computing`
  - Code: `CS401`
  - Description: `AWS, Azure, and GCP fundamentals`
  - Semester: `2025-Spring`
  - Credits: `3`
  - Course Type: `elective`
- [ ] Submit
- [ ] ✅ New course appears in the list

---

## 6 — Attendance Tracker (Pillar III)

> Login as **student1@iitmandi.ac.in**

- [ ] Click **Attendance** in sidebar
- [ ] ✅ Page title: "Attendance Tracker"
- [ ] ✅ Summary cards visible for enrolled courses (CS201 and CS301 from seed)
- [ ] ✅ Each card shows: course code, course name, percentage, progress bar, attended/total count

### 6.1 Check Percentage
- [ ] ✅ CS201 (DSA) shows a percentage (some present, some absent from seed)
- [ ] ✅ CS301 (ML) shows 100% (all marked present in seed)
- [ ] ✅ Color coding: ≥75% = green, 50-74% = amber, <50% = red

### 6.2 Mark Attendance
- [ ] Select a course from the dropdown (e.g. CS201)
- [ ] Select today's date
- [ ] Select status: **present**
- [ ] Click **Mark**
- [ ] ✅ Summary card updates (total classes +1, present +1)

### 6.3 Mark as Absent
- [ ] Select same or different course
- [ ] Change date to yesterday (or another date)
- [ ] Select status: **absent**
- [ ] Click **Mark**
- [ ] ✅ Summary updates (total +1, percentage may decrease)

### 6.4 View History
- [ ] Click on a course summary card
- [ ] ✅ Attendance history table appears below
- [ ] ✅ Each row shows date and status badge (green=present, red=absent, amber=late)

---

## 7 — Resources / Vault of Knowledge (Pillar III)

> Login as **student1@iitmandi.ac.in**

- [ ] Click **Resources** in sidebar
- [ ] ✅ Page title: "Vault of Knowledge"
- [ ] ✅ 5 seeded resources visible in grid layout
- [ ] ✅ Each card shows: icon, title, course code, resource type, year, tags, uploader name

### 7.1 Filter Resources
- [ ] Click **PYQ** filter → only PYQ resources shown
- [ ] Click **Notes** filter → only notes shown
- [ ] Click **All Types** → all resources shown
- [ ] If course filter dropdown appears, select `CS201` → only CS201 resources
- [ ] Reset to All

### 7.2 Upload a Resource
- [ ] Click **Upload Resource** button
- [ ] ✅ Upload form appears
- [ ] Fill in:
  - Title: `ML Assignment 2 Solutions`
  - File URL: `https://drive.google.com/example`
  - Course Code: `CS301`
  - Year: `2025`
  - Resource Type: `assignment`
  - Tags: `neural-networks,backpropagation`
- [ ] Click **Upload**
- [ ] ✅ New resource card appears in the grid

### 7.3 Delete Own Resource
- [ ] Find the resource just uploaded
- [ ] Click the 🗑️ delete icon
- [ ] ✅ Resource removed from grid

---

## 8 — Academic Calendar / Chronos Calendar (Pillar III)

> Login as **student1@iitmandi.ac.in**

- [ ] Click **Calendar** in sidebar
- [ ] ✅ Page title: "Chronos Calendar"
- [ ] ✅ 6 seeded events visible, grouped by month
- [ ] ✅ Each event shows: icon, title, event type badge, date, course name (if applicable)
- [ ] ✅ Color coding: exam=red, assignment=amber, holiday=green, deadline=purple, event=blue

### 8.1 Filter Events
- [ ] Click **exam** filter → only exams shown
- [ ] Click **holiday** filter → only holidays shown
- [ ] Click **All** → all events shown

### 8.2 Student Cannot Create Events
- [ ] ✅ "Add Event" button is **NOT** visible

### 8.3 Faculty Creates Event
> Login as **faculty1@iitmandi.ac.in**

- [ ] Click **Calendar** → Click **Add Event**
- [ ] ✅ Form appears
- [ ] Fill in:
  - Title: `DSA Quiz 3`
  - Date: (pick a date 5 days from now)
  - Type: `exam`
- [ ] Click **Create Event**
- [ ] ✅ Event appears in the timeline

---

## 9 — Tasks / Scholar's Ledger (Pillar IV)

> Login as **student1@iitmandi.ac.in**

- [ ] Click **Tasks** in sidebar
- [ ] ✅ Page title: "Scholar's Ledger"
- [ ] ✅ Stats row shows: Total Tasks, In Progress, Completed counts
- [ ] ✅ 4 seeded tasks visible (for student1)

### 9.1 Filter Tasks
- [ ] Click **in progress** filter → only in-progress tasks shown
- [ ] Click **done** filter → only completed tasks shown
- [ ] Click **All** → all tasks shown

### 9.2 Create a Task
- [ ] Click **New Task** button
- [ ] Fill in:
  - Title: `Read Chapter 7 for DSA`
  - Description: `Graph algorithms - BFS, DFS, Dijkstra`
  - Due Date: (3 days from now)
  - Category: `exam_prep`
  - Priority: `high`
- [ ] Click **Create**
- [ ] ✅ New task appears in the list

### 9.3 Toggle Task Status
- [ ] Find a task with status **todo**
- [ ] Click the circle icon on the left → status changes to **in_progress** (blue dot appears)
- [ ] Click again → status changes to **done** (green check, text strikethrough, opacity reduced)
- [ ] Click again → cycles back to **todo**
- [ ] ✅ Stats row updates with each change

### 9.4 Delete a Task
- [ ] Click the 🗑️ delete icon on any task
- [ ] ✅ Task removed from list, total count decreases

### 9.5 Overdue Detection
- [ ] ✅ Tasks with past due dates (and not "done") show due date in red

---

## 10 — Internships (Pillar IV)

### 10.1 View Internships (Student)
> Login as **student1@iitmandi.ac.in**

- [ ] Click **Internships** in sidebar
- [ ] ✅ 4 seeded internships visible
- [ ] ✅ Each shows: title, company, description, location, stipend, deadline, required skills, duration, poster name

### 10.2 Apply to Internship
- [ ] Find an internship not yet applied to (e.g. "Data Analyst Intern")
- [ ] Click **Apply** button
- [ ] ✅ Button changes to show applied status

### 10.3 View My Applications
- [ ] Check applications section / tab
- [ ] ✅ Shows applied internships with statuses (submitted, shortlisted, etc.)
- [ ] ✅ "ML Research Intern" shows **shortlisted** (from seed)
- [ ] ✅ "Full Stack Developer Intern" shows **submitted** (from seed)

### 10.4 Faculty Manages Applications
> Login as **faculty1@iitmandi.ac.in**

- [ ] Click **Internships**
- [ ] Click on "ML Research Intern" (posted by faculty1)
- [ ] ✅ Can see list of applications
- [ ] Change an application status (e.g. from "shortlisted" to "accepted")
- [ ] ✅ Status updates successfully

---

## 11 — Lost & Found / Relic Recovery (Pillar V)

> Login as **student1@iitmandi.ac.in**

- [ ] Click **Lost & Found** in sidebar
- [ ] ✅ Page title: "Relic Recovery"
- [ ] ✅ 4 seeded items visible in grid
- [ ] ✅ Each item shows: icon, title, LOST/FOUND badge, status badge, description, location, poster name

### 11.1 Filter Items
- [ ] Click **lost** filter → only lost items shown (Calculator, Hoodie)
- [ ] Click **found** filter → only found items shown (Water Bottle, ID Card)
- [ ] Click **All** → all items shown

### 11.2 Report a Lost Item
- [ ] Click **Report Item** button
- [ ] Fill in:
  - Item Name: `USB-C Charger`
  - Location: `Library 2nd Floor`
  - Type: `lost`
  - Category: `electronics`
  - Description: `White 65W charger, Anker brand`
- [ ] Click **Submit**
- [ ] ✅ New item appears in grid with LOST badge

### 11.3 Claim an Item
> Login as **student2@iitmandi.ac.in** (`student2@iitmandi.ac.in` / `password123`)

- [ ] Click **Lost & Found**
- [ ] Find "Student ID Card" (posted by student3, type: found)
- [ ] ✅ "This is mine" button visible
- [ ] Click **This is mine**
- [ ] ✅ Item status changes to **claimed**
- [ ] ✅ Claim button disappears

### 11.4 Cannot Claim Own Item
> Login as **student1@iitmandi.ac.in**

- [ ] Find "Blue Water Bottle" (posted by student1)
- [ ] ✅ No claim button visible (cannot claim your own item)

---

## 12 — Forum / Hall of Echoes (Pillar VI)

> Login as **student1@iitmandi.ac.in**

- [ ] Click **Forum** in sidebar
- [ ] ✅ Page title: "Hall of Echoes"
- [ ] ✅ 4 seeded posts visible in Reddit-style layout
- [ ] ✅ Each post shows: vote arrows, score, category badge, author, title, content preview, comment count, date

### 12.1 Filter by Category
- [ ] Click **academics** filter → only academic posts shown
- [ ] Click **campus life** filter → only campus life posts shown
- [ ] Click **All** → all posts shown

### 12.2 Upvote / Downvote
- [ ] Click the ⬆ upvote arrow on "Campus WiFi keeps disconnecting"
- [ ] ✅ Vote count increases by 1
- [ ] Click the ⬇ downvote arrow on any post
- [ ] ✅ Downvote count increases

### 12.3 View Post Detail
- [ ] Click on "Best resources for learning ML?"
- [ ] ✅ Full post content displayed
- [ ] ✅ Comments section shows 2 seeded comments
- [ ] ✅ Each comment shows: author name, date, content, upvotes
- [ ] ✅ Upvote/downvote buttons visible on the post

### 12.4 Add a Comment
- [ ] Type in comment box: `Thanks for the recommendations! I'll start with Andrew Ng's course.`
- [ ] Click **Post** (or press Enter)
- [ ] ✅ Comment appears in the comments list

### 12.5 Create a New Post
- [ ] Click **Back to Forum** to return to list
- [ ] Click **New Post** button
- [ ] Fill in:
  - Title: `Study group for Linear Algebra?`
  - Content: `Looking to form a study group for MA201. Meeting twice a week in the library. Anyone interested?`
  - Category: `academics`
- [ ] Click **Post**
- [ ] ✅ New post appears in the forum list

---

## 13 — User Management (Admin Only)

> Login as **admin@iitmandi.ac.in**

- [ ] Click **Users** in sidebar
- [ ] ✅ All 8 seeded users visible
- [ ] ✅ Each user shows: name, email, role, department

### 13.1 Filter by Role
- [ ] Filter by **student** → only 3 students shown
- [ ] Filter by **faculty** → only 2 faculty shown
- [ ] Clear filter → all users shown

### 13.2 Edit a User
- [ ] Click edit on a student user
- [ ] Change department to `Data Science`
- [ ] Save changes
- [ ] ✅ Department updates in the list

### 13.3 Non-Admin Cannot Access
> Login as **student1@iitmandi.ac.in**

- [ ] Navigate manually to `http://localhost:3000/dashboard/users`
- [ ] ✅ Page either redirects or shows access denied / empty

---

## 14 — Profile Page

> Login as **student1@iitmandi.ac.in**

- [ ] Click **Profile** in sidebar
- [ ] ✅ Shows user info: name, email, role, department, member since date

---

## 15 — Cross-Feature Integration Tests

### 15.1 Grievance → Forum Connection
> Login as **student1@iitmandi.ac.in**

- [ ] Submit a grievance about WiFi
- [ ] Go to Forum → find the "Campus WiFi keeps disconnecting" post
- [ ] ✅ A comment from seed references filing a grievance, showing conceptual link

### 15.2 Course → Attendance → Calendar Flow
- [ ] Go to **Courses** → verify enrolled in CS201
- [ ] Go to **Attendance** → verify CS201 summary card exists
- [ ] Go to **Calendar** → verify "DSA Midsem Exam" event exists for CS201
- [ ] ✅ All three pages reference the same course consistently

### 15.3 Internship Application Lifecycle
> Login as **student1@iitmandi.ac.in**

- [ ] Go to **Internships** → Apply to "Data Analyst Intern"
- [ ] ✅ Application status = submitted

> Login as **faculty2@iitmandi.ac.in** (`faculty2@iitmandi.ac.in` / `password123`)

- [ ] Go to **Internships** → View applications for "Data Analyst Intern"
- [ ] Update student1's application to **under_review**
- [ ] Update to **shortlisted**
- [ ] Update to **accepted**

> Login as **student1@iitmandi.ac.in**

- [ ] Go to **Internships** → My Applications
- [ ] ✅ "Data Analyst Intern" now shows **accepted**

---

## 16 — Responsive Design

- [ ] Resize browser to mobile width (~375px)
- [ ] ✅ Sidebar collapses to hamburger menu
- [ ] Click hamburger → sidebar opens as overlay
- [ ] Click outside sidebar → it closes
- [ ] ✅ All pages are scrollable and readable on mobile
- [ ] Test these pages specifically on mobile:
  - [ ] Announcements — cards stack vertically
  - [ ] Attendance — summary cards stack, form wraps
  - [ ] Resources — grid becomes single column
  - [ ] Tasks — task items remain functional
  - [ ] Forum — posts stack with vote controls

---

## 17 — Backend API Verification (Optional — via Swagger)

- [ ] Open `http://127.0.0.1:8000/docs` in browser
- [ ] ✅ Swagger UI loads with all API groups:
  - auth, dashboard, grievances, courses, internships, users,
    attendance, resources, calendar, tasks, lost-found, announcements, forum
- [ ] Click **Authorize** → enter a JWT token obtained from login
- [ ] Test `/api/announcements/` GET → returns 5 announcements
- [ ] Test `/api/forum/posts` GET → returns 4 posts
- [ ] Test `/api/tasks/` GET → returns tasks for authenticated user
- [ ] Test `/api/attendance/summary` GET → returns attendance summaries
- [ ] Test `/api/lost-found/` GET → returns 4+ items
- [ ] Test `/api/calendar/events` GET → returns 6 events
- [ ] Test `/api/resources/` GET → returns 5 resources

---

## Quick Reference — All Test Accounts

| Role      | Email                        | Name              | Department            |
|-----------|------------------------------|-------------------|-----------------------|
| Admin     | admin@iitmandi.ac.in         | Dr. Arjun Mehta   | Administration        |
| Authority | authority@iitmandi.ac.in     | Prof. Sunita Sharma | Dean of Students    |
| Authority | authority2@iitmandi.ac.in    | Prof. Vikram Joshi | Hostel Warden        |
| Faculty   | faculty1@iitmandi.ac.in      | Dr. Rajesh Kumar  | Computer Science      |
| Faculty   | faculty2@iitmandi.ac.in      | Dr. Priya Nair    | Electrical Engineering|
| Student   | student1@iitmandi.ac.in      | Aarav Patel       | Computer Science      |
| Student   | student2@iitmandi.ac.in      | Diya Gupta        | Electrical Engineering|
| Student   | student3@iitmandi.ac.in      | Kabir Singh       | Mechanical Engineering|

> **Password for all accounts:** `password123`

---

## Result Tracker

| # | Feature             | Status | Notes |
|---|---------------------|--------|-------|
| 1 | Auth & Roles        | ⬜     |       |
| 2 | Dashboard           | ⬜     |       |
| 3 | Announcements       | ⬜     |       |
| 4 | Grievances          | ⬜     |       |
| 5 | Courses             | ⬜     |       |
| 6 | Attendance          | ⬜     |       |
| 7 | Resources           | ⬜     |       |
| 8 | Calendar            | ⬜     |       |
| 9 | Tasks               | ⬜     |       |
| 10| Internships         | ⬜     |       |
| 11| Lost & Found        | ⬜     |       |
| 12| Forum               | ⬜     |       |
| 13| User Management     | ⬜     |       |
| 14| Profile             | ⬜     |       |
| 15| Integration Tests   | ⬜     |       |
| 16| Responsive Design   | ⬜     |       |
| 17| API Swagger         | ⬜     |       |
