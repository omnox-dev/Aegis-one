"""Seed the database with demo data for all 7 Pillars."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timezone, date, timedelta
from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password

# Import ALL models
from app.models.user import User
from app.models.grievance import Grievance, GrievanceComment
from app.models.course import Course, Enrollment
from app.models.internship import Internship, Application
from app.models.attendance import Attendance
from app.models.resource import Resource
from app.models.academic_event import AcademicEvent
from app.models.task import Task
from app.models.lost_found import LostFoundItem
from app.models.announcement import Announcement
from app.models.forum import ForumPost, ForumComment
from app.models.caravan_mercenary import CaravanPool, MercenaryGig
from app.models.clubs import Club, ClubMember, ClubEvent, ClubAnnouncement
from app.models.location import CampusLocation
from app.models.incident import Incident

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Clear all
for model in [ClubAnnouncement, ClubEvent, Incident, CampusLocation, ClubMember, Club, MercenaryGig, CaravanPool, ForumComment, ForumPost, Announcement, LostFoundItem, Task, AcademicEvent, Resource, Attendance, Application, Enrollment, GrievanceComment, Grievance, Internship, Course, User]:
    db.query(model).delete()
db.commit()

print("[SEED] Seeding AEGIS Platform...")

# ── USERS ──
pwd = hash_password("password123")
users = [
    User(id=1, email="admin@iitmandi.ac.in", name="Dr. Arjun Mehta", hashed_password=pwd, role="admin", department="Administration"),
    User(id=2, email="authority@iitmandi.ac.in", name="Prof. Sunita Sharma", hashed_password=pwd, role="authority", department="Dean of Students"),
    User(id=3, email="faculty1@iitmandi.ac.in", name="Dr. Rajesh Kumar", hashed_password=pwd, role="faculty", department="Computer Science"),
    User(id=4, email="faculty2@iitmandi.ac.in", name="Dr. Priya Nair", hashed_password=pwd, role="faculty", department="Electrical Engineering"),
    User(id=5, email="student1@iitmandi.ac.in", name="Aarav Patel", hashed_password=pwd, role="student", department="Computer Science"),
    User(id=6, email="student2@iitmandi.ac.in", name="Diya Gupta", hashed_password=pwd, role="student", department="Electrical Engineering"),
    User(id=7, email="student3@iitmandi.ac.in", name="Kabir Singh", hashed_password=pwd, role="student", department="Mechanical Engineering"),
    User(id=8, email="authority2@iitmandi.ac.in", name="Prof. Vikram Joshi", hashed_password=pwd, role="authority", department="Hostel Warden"),
]
for u in users:
    db.add(u)
db.commit()
print("  [OK] 8 users created")

# ── COURSES (Pillar III) ──
courses = [
    Course(id=1, name="Data Structures & Algorithms", code="CS201", description="Fundamental data structures, sorting algorithms, and complexity analysis.", semester="2025-Spring", credits=4, course_type="major", faculty_id=3),
    Course(id=2, name="Machine Learning", code="CS301", description="Supervised and unsupervised learning, neural networks, and model evaluation.", semester="2025-Spring", credits=4, course_type="major", faculty_id=3),
    Course(id=3, name="Digital Signal Processing", code="EE301", description="Fourier analysis, filter design, and signal processing applications.", semester="2025-Spring", credits=3, course_type="major", faculty_id=4),
    Course(id=4, name="Linear Algebra", code="MA201", description="Vector spaces, eigenvalues, and matrix decomposition.", semester="2025-Spring", credits=3, course_type="minor", faculty_id=3),
    Course(id=5, name="Technical Writing", code="HS101", description="Academic writing, report formatting, and research presentation.", semester="2025-Spring", credits=2, course_type="elective", faculty_id=4),
    Course(id=6, name="Computer Networks Lab", code="CS202L", description="Hands-on networking experiments with TCP/IP, routing, and socket programming.", semester="2025-Spring", credits=1, course_type="lab", faculty_id=3),
]
for c in courses:
    db.add(c)
db.commit()
print("  [OK] 6 courses created")

# ── ENROLLMENTS ──
enrollments = [
    Enrollment(student_id=5, course_id=1), Enrollment(student_id=5, course_id=2),
    Enrollment(student_id=5, course_id=4), Enrollment(student_id=5, course_id=6),
    Enrollment(student_id=6, course_id=1), Enrollment(student_id=6, course_id=3),
    Enrollment(student_id=6, course_id=5),
    Enrollment(student_id=7, course_id=1), Enrollment(student_id=7, course_id=4),
]
for e in enrollments:
    db.add(e)
db.commit()
print("  [OK] 9 enrollments created")

# ── GRIEVANCES (Pillar II) ──
today = datetime.now(timezone.utc)
grievances = [
    Grievance(id=1, title="Wi-Fi connectivity issues in Hostel Block C", description="The Wi-Fi in Block C has been extremely unreliable for the past 2 weeks. Students are unable to attend online classes or submit assignments on time.", category="infrastructure", priority="high", status="in_review", location="Hostel Block C", submitted_by=5, assigned_to=2),
    Grievance(id=2, title="Mess food quality deterioration", description="The quality of food served in the North Mess has significantly declined. Multiple students have reported hygiene issues.", category="food", priority="urgent", status="pending", location="North Mess", is_anonymous=True, submitted_by=6),
    Grievance(id=3, title="Library closing early on weekends", description="The library closes at 6 PM on weekends whereas it should be open till 10 PM as per the academic policy.", category="academic", priority="medium", status="resolved", location="Central Library", submitted_by=7, assigned_to=2),
    Grievance(id=4, title="Broken AC in Lecture Hall 3", description="The air conditioning in LH-3 has not been working for over a month. The temperature during afternoon classes becomes unbearable.", category="infrastructure", priority="high", status="in_progress", location="Lecture Hall 3", submitted_by=5),
    Grievance(id=5, title="Insufficient parking near academic blocks", description="There is a severe shortage of parking spots near the academic buildings, causing students to park far away and arrive late to classes.", category="infrastructure", priority="low", status="pending", location="Academic Block Parking", submitted_by=6),
]
for g in grievances:
    db.add(g)
db.commit()

# Grievance comments
comments = [
    GrievanceComment(grievance_id=1, user_id=2, content="We have notified the IT department. A technician will visit Block C tomorrow."),
    GrievanceComment(grievance_id=1, user_id=5, content="Thank you for the update. The issue seems to be with the router on the 3rd floor specifically."),
    GrievanceComment(grievance_id=3, user_id=2, content="Library hours have been extended to 10 PM on weekends effective immediately."),
    GrievanceComment(grievance_id=3, user_id=7, content="Thank you! This is very helpful for exam preparation."),
    GrievanceComment(grievance_id=4, user_id=1, content="Maintenance has been scheduled for next week. Temporary fans will be placed in LH-3."),
]
for c in comments:
    db.add(c)
db.commit()
print("  [OK] 5 grievances + 5 comments created")

# ── INTERNSHIPS (Pillar IV) ──
internships = [
    Internship(id=1, title="ML Research Intern", company="IIT Mandi - AI Lab", description="Work on cutting-edge NLP research. Build transformer models for low-resource Indian languages.", location="IIT Mandi Campus", stipend=15000, role_type="research", required_skills="Python, PyTorch, NLP, Transformers", duration="3 months", deadline=date.today() + timedelta(days=30), posted_by=3),
    Internship(id=2, title="Full Stack Developer Intern", company="TechCorp India", description="Build scalable web applications using React and Node.js for enterprise clients.", location="Bangalore", stipend=25000, role_type="internship", required_skills="React, Node.js, PostgreSQL, TypeScript", duration="6 months", deadline=date.today() + timedelta(days=45), posted_by=3),
    Internship(id=3, title="Embedded Systems Research", company="IIT Mandi - Robotics Lab", description="Design and implement control systems for autonomous drones.", location="IIT Mandi Campus", stipend=12000, role_type="research", required_skills="C/C++, MATLAB, Arduino, ROS", duration="4 months", deadline=date.today() + timedelta(days=20), posted_by=4),
    Internship(id=4, title="Data Analyst Intern", company="Analytics Pro", description="Analyze large datasets, create dashboards, and derive actionable business insights.", location="Remote", stipend=20000, role_type="internship", required_skills="Python, SQL, Tableau, Statistics", duration="3 months", deadline=date.today() + timedelta(days=60), posted_by=4),
]
for i in internships:
    db.add(i)
db.commit()

applications = [
    Application(student_id=5, internship_id=1, status="shortlisted"),
    Application(student_id=5, internship_id=2, status="submitted"),
    Application(student_id=6, internship_id=1, status="submitted"),
    Application(student_id=7, internship_id=3, status="accepted"),
]
for a in applications:
    db.add(a)
db.commit()
print("  [OK] 4 internships + 4 applications created")

# ── ATTENDANCE (Pillar III) ──
att_dates = [date.today() - timedelta(days=i) for i in range(10)]
for d in att_dates:
    if d.weekday() < 5:  # weekdays only
        db.add(Attendance(student_id=5, course_id=1, date=d, status="present" if d.day % 3 != 0 else "absent"))
        db.add(Attendance(student_id=5, course_id=2, date=d, status="present"))
db.commit()
print("  [OK] Attendance records created")

# ── RESOURCES (Pillar III - Vault of Knowledge) ──
resources = [
    Resource(title="DSA Midsem Paper 2024", file_url="/uploads/dsa_midsem_2024.pdf", course_code="CS201", year="2024", exam_type="midsem", resource_type="pyq", tags="sorting,trees,graphs", uploaded_by=5),
    Resource(title="DSA Endsem Paper 2024", file_url="/uploads/dsa_endsem_2024.pdf", course_code="CS201", year="2024", exam_type="endsem", resource_type="pyq", tags="dp,greedy,advanced", uploaded_by=6),
    Resource(title="ML Lecture Notes - Week 1-4", file_url="/uploads/ml_notes_w1_4.pdf", course_code="CS301", year="2025", exam_type="notes", resource_type="notes", tags="regression,classification,svm", uploaded_by=5),
    Resource(title="Linear Algebra Summary", file_url="/uploads/la_summary.pdf", course_code="MA201", year="2025", resource_type="notes", tags="eigenvalues,matrices,vector-spaces", uploaded_by=7),
    Resource(title="DSP Quiz 1 Paper 2023", file_url="/uploads/dsp_quiz1_2023.pdf", course_code="EE301", year="2023", exam_type="quiz", resource_type="pyq", tags="fourier,laplace", uploaded_by=6),
]
for r in resources:
    db.add(r)
db.commit()
print("  [OK] 5 resources created")

# ── ACADEMIC EVENTS (Pillar III - Chronos Calendar) ──
events = [
    AcademicEvent(title="DSA Midsem Exam", event_date=date.today() + timedelta(days=14), event_type="exam", course_id=1, created_by=3),
    AcademicEvent(title="ML Assignment 3 Due", event_date=date.today() + timedelta(days=7), event_type="assignment", course_id=2, created_by=3),
    AcademicEvent(title="Republic Day Holiday", event_date=date(2026, 1, 26), event_type="holiday", created_by=1),
    AcademicEvent(title="Semester End", event_date=date.today() + timedelta(days=60), event_type="deadline", created_by=1),
    AcademicEvent(title="DSP Lab Quiz", event_date=date.today() + timedelta(days=5), event_type="exam", course_id=3, created_by=4),
    AcademicEvent(title="Technical Festival - Exodia", event_date=date.today() + timedelta(days=21), event_type="event", created_by=1, description="Annual technical festival with workshops, hackathons, and competitions."),
]
for e in events:
    db.add(e)
db.commit()
print("  [OK] 6 academic events created")

# ── TASKS (Pillar IV - Scholar's Ledger) ──
tasks = [
    Task(title="Complete DSA Assignment 4", description="Implement AVL trees and Red-Black trees.", due_date=date.today() + timedelta(days=3), category="assignment", status="in_progress", priority="high", user_id=5),
    Task(title="ML Project Proposal", description="Write the project proposal for sentiment analysis model.", due_date=date.today() + timedelta(days=10), category="project", status="todo", priority="medium", user_id=5),
    Task(title="Prepare for Midsems", description="Review chapters 1-6 for DSA midsem.", due_date=date.today() + timedelta(days=14), category="exam_prep", status="todo", priority="high", user_id=5),
    Task(title="Update Resume", description="Add recent project and internship experience.", due_date=date.today() + timedelta(days=5), category="personal", status="done", priority="low", user_id=5),
    Task(title="DSP Lab Report", due_date=date.today() + timedelta(days=2), category="assignment", status="in_progress", priority="high", user_id=6),
]
for t in tasks:
    db.add(t)
db.commit()
print("  [OK] 5 tasks created")

# ── LOST & FOUND (Pillar V) ──
lost_found = [
    LostFoundItem(title="Blue Water Bottle", description="Found near South Mess entrance. Has an IIT Mandi sticker.", location="South Mess", category="other", item_type="found", posted_by=5),
    LostFoundItem(title="Scientific Calculator (Casio fx-991EX)", description="Lost somewhere between LH-1 and Library. Silver colored.", location="Academic Block", category="electronics", item_type="lost", posted_by=6),
    LostFoundItem(title="Student ID Card", description="Found ID card of a B.Tech 2023 batch student near parking.", location="Main Parking", category="id_cards", item_type="found", posted_by=7),
    LostFoundItem(title="Black Hoodie", description="Left in LH-3 after evening class on Monday.", location="Lecture Hall 3", category="clothing", item_type="lost", posted_by=5),
]
for lf in lost_found:
    db.add(lf)
db.commit()
print("  [OK] 4 lost & found items created")

# ── ANNOUNCEMENTS (Pillar VII) ──
announcements = [
    Announcement(title="Mid-Semester Exam Schedule Released", content="The mid-semester examination schedule for Spring 2025 has been released. Please check the academic calendar for details. Exams will begin from March 10th.", category="academic", pinned=True, posted_by=1),
    Announcement(title="Campus Recruitment Drive - Week 3", content="TechCorp and Analytics Pro will be visiting campus for recruitment. Eligible students should register on the placement portal by Feb 20th.", category="events", posted_by=2),
    Announcement(title="Library Renovation Notice", content="The central library will undergo renovation from March 1-5. During this period, the reading room in Block A will be available as an alternative.", category="administrative", posted_by=1),
    Announcement(title="Annual Sports Meet Registration", content="Register for the Annual Sports Meet 2025. Events include cricket, football, badminton, athletics, and chess. Last date: Feb 25th.", category="events", posted_by=2),
    Announcement(title="Emergency: Water Supply Disruption", content="Water supply to Hostel Blocks A-D will be disrupted on Feb 16 from 10 AM to 4 PM due to maintenance work. Please store water in advance.", category="emergency", pinned=True, posted_by=1),
]
for a in announcements:
    db.add(a)
db.commit()
print("  [OK] 5 announcements created")

# ── FORUM (Pillar VI - Hall of Echoes) ──
posts = [
    ForumPost(id=1, title="Best resources for learning ML?", content="I'm starting CS301 next semester. What are the best resources (books, courses, YouTube channels) to prepare beforehand? Any tips from seniors who've taken this course?", category="academics", author_id=6, upvotes=12, downvotes=1),
    ForumPost(id=2, title="Campus WiFi keeps disconnecting", content="Is anyone else experiencing constant WiFi drops in Block B? It's been happening since last week and it's really affecting my work. Should we file a collective grievance?", category="tech_support", author_id=5, upvotes=25, downvotes=0),
    ForumPost(id=3, title="Organize a hackathon this semester?", content="Would anyone be interested in organizing an inter-hostel hackathon? We could do a 24-hour event with prizes from the tech club budget. Looking for co-organizers!", category="events", author_id=7, upvotes=18, downvotes=2),
    ForumPost(id=4, title="Tips for surviving first winter in Mandi", content="First year here and the cold is no joke! Any tips for staying warm? Best places to buy winter gear locally?", category="campus_life", author_id=6, upvotes=8, downvotes=0),
]
for p in posts:
    db.add(p)
db.commit()

forum_comments = [
    ForumComment(post_id=1, author_id=5, content="Andrew Ng's ML course on Coursera is a must. Also check out 3Blue1Brown for the math intuition.", upvotes=8),
    ForumComment(post_id=1, author_id=7, content="The course textbook (ISLR) is actually quite good. Don't skip the exercises!", upvotes=5),
    ForumComment(post_id=2, author_id=7, content="Same issue in Block C! I've already filed a grievance. You can track it on the platform.", upvotes=15),
    ForumComment(post_id=2, author_id=6, content="IT department said they're upgrading routers next week. Fingers crossed!", upvotes=10),
    ForumComment(post_id=3, author_id=5, content="I'm in! Have experience organizing events. DM me.", upvotes=6),
    ForumComment(post_id=4, author_id=5, content="Get a good room heater and thermal innerwear. The market in town has decent options.", upvotes=4),
]
for fc in forum_comments:
    db.add(fc)
db.commit()
print("  [OK] 4 forum posts + 6 comments created")

# ── THE COMMONS (Pillar V) - Caravan & Mercenary ──
caravans = [
    CaravanPool(destination="Mandi Bus Stand", travel_date=datetime.now(timezone.utc) + timedelta(hours=5), available_seats=3, estimated_cost=400, posted_by=5),
    CaravanPool(destination="Kullu Airport", travel_date=datetime.now(timezone.utc) + timedelta(days=2), available_seats=2, estimated_cost=2500, posted_by=6),
]
for c in caravans: db.add(c)

mercenaries = [
    MercenaryGig(title="UI/UX Design for Hackathon", description="Need a clean dashboard mockup for our project.", category="design", budget="₹1000", posted_by=5),
    MercenaryGig(title="Python Debugging Help", description="Fixing a circular import in a FastAPI project.", category="coding", budget="Treat at North Mess", posted_by=6),
]
for m in mercenaries: db.add(m)
db.commit()
print("  [OK] 2 caravans + 2 mercenary gigs created")

# ── THE SPIRIT (Pillar VII) - Clubs ──
clubs = [
    Club(id=1, name="Kamand Coding Club", description="The official coding club of IIT Mandi. We organize hackathons and workshops.", category="technical", lead_id=3),
    Club(id=2, name="Music Society", description="For the lovers of rhythm and melody.", category="cultural", lead_id=3),
]
for c in clubs: db.add(c)
db.commit()

memberships = [
    ClubMember(club_id=1, user_id=5, role="coordinator"),
    ClubMember(club_id=1, user_id=6, role="member"),
    ClubMember(club_id=2, user_id=7, role="member"),
]
for m in memberships: db.add(m)
db.commit()
print("  [OK] 2 clubs + 3 memberships created")

# ── Guild Events & Dispatches ──
club_events = [
    ClubEvent(club_id=1, title="Competitive Programming Sprints", description="Join us for a 3-hour intense coding session.", event_date=datetime(2026, 2, 25, 18, 0), location="A10 Block"),
    ClubEvent(club_id=2, title="Drama Night Rehearsals", description="Preparation for the upcoming spring fest.", event_date=datetime(2026, 2, 28, 20, 0), location="Auditorium"),
]
for e in club_events: db.add(e)

club_ann = [
    ClubAnnouncement(club_id=1, title="Recruitment Phase 1 Results", content="Check the portal for the list of shortlisted candidates for the Core team."),
    ClubAnnouncement(club_id=2, title="New Equipment Acquired", content="We have successfully procured a new sound system for all upcoming performances."),
]
for a in club_ann: db.add(a)

db.commit()
print("  [OK] Club events and dispatches seeded")

# ── CONNECTION (Pillar VI) - Pathfinder's Map ──
locations = [
    CampusLocation(name="North Campus Library", description="Main central library for UG/PG students.", category="Facility", latitude=30, longitude=40),
    CampusLocation(name="A10 Block", description="CSE and EE Department building.", category="Academic", latitude=45, longitude=50),
    CampusLocation(name="B1 Mess", description="North campus central dining hall.", category="Mess", latitude=35, longitude=30),
    CampusLocation(name="Cedar Mess", description="South campus mess hall.", category="Mess", latitude=70, longitude=65),
    CampusLocation(name="Medical Center", description="24/7 emergency medical services.", category="Medic", latitude=50, longitude=45),
    CampusLocation(name="D2 Hostel", description="Student accommodation with valley view.", category="Hostel", latitude=60, longitude=75),
]
for l in locations: db.add(l)
db.commit()
print("  [OK] 6 campus locations created")

# ── Hall of Echoes (Forum) Initial Posts ──
forum_posts = [
    ForumPost(title="Best place for night snacks in Kamand?", content="North campus is great, but South campus mess has those parathas. Thoughts?", category="campus_life", author_id=5, upvotes=12),
    ForumPost(title="Linear Algebra survival guide", content="Prof is fast. Anyone want to form a study group for the mid-sem?", category="academics", author_id=6, upvotes=8),
]
for p in forum_posts: db.add(p)
db.commit()
print("  [OK] 2 forum posts created")

db.close()
print("\n[DONE] AEGIS Platform seeded successfully!")
print("\nTest Credentials (password: password123):")
print("  Admin:     admin@iitmandi.ac.in")
print("  Authority:  authority@iitmandi.ac.in")
print("  Faculty:    faculty1@iitmandi.ac.in")
print("  Student:    student1@iitmandi.ac.in")
