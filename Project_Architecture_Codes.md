# System Architecture and UML Diagrams

## 1. System Architecture (DOT Code)

This DOT code represents the high-level architecture of the application, showing the interaction between the Frontend (Next.js), Backend (FastAPI), and Database.

```dot
digraph SystemArchitecture {
    rankdir=LR;
    node [shape=box, style=filled, fontname="Arial"];

    subgraph cluster_frontend {
        label = "Frontend (Next.js)";
        style = filled;
        color = lightblue;
        node [color=white];
        NextJS_Page [label="Pages\n(React Components)"];
        API_Client [label="API Client\n(Axios/Fetch)"];
        NextJS_Page -> API_Client;
    }

    subgraph cluster_backend {
        label = "Backend (FastAPI)";
        style = filled;
        color = lightgreen;
        node [color=white];
        API_Gateway [label="API Router\n(FastAPI)"];
        Auth_Service [label="Auth Service\n(JWT)"];
        Business_Logic [label="Services/Logic"];
        ORM_Layer [label="ORM\n(SQLAlchemy)"];

        API_Gateway -> Auth_Service;
        API_Gateway -> Business_Logic;
        Business_Logic -> ORM_Layer;
    }

    subgraph cluster_database {
        label = "Data Layer";
        style = filled;
        color = lightgrey;
        node [shape=cylinder, color=white, style=filled, fillcolor=white];
        Database [label="PostgreSQL\nDatabase"];
    }

    User [shape=circle, label="User\n(Browser/Mobile)"];

    User -> NextJS_Page [label="Interacts"];
    API_Client -> API_Gateway [label="HTTP/JSON Requests"];
    ORM_Layer -> Database [label="SQL Queries"];
}
```

## 2. Database Entity Relationship Diagram (PlantUML)

This PlantUML code details the database schema based on the SQLAlchemy models found in `backend/app/models/`.

```plantuml
@startuml
!theme plain
hide circle
skinparam linetype ortho

entity "User" as users {
  *id : Integer
  --
  email : String
  hashed_password : String
  role : String
  department : String
}

entity "Announcement" as announcements {
  *id : Integer
  --
  title : String
  content : Text
  category : String
  posted_by : Integer <<FK>>
}

entity "Attendance" as attendance {
  *id : Integer
  --
  student_id : Integer <<FK>>
  course_id : Integer <<FK>>
  date : Date
  status : String
}

entity "Course" as courses {
  *id : Integer
  --
  name : String
  code : String
  faculty_id : Integer <<FK>>
}

entity "Enrollment" as enrollments {
  *id : Integer
  --
  student_id : Integer <<FK>>
  course_id : Integer <<FK>>
}

entity "Club" as clubs {
  *id : Integer
  --
  name : String
  lead_id : Integer <<FK>>
}

entity "ClubMember" as club_members {
  *id : Integer
  --
  club_id : Integer <<FK>>
  user_id : Integer <<FK>>
  role : String
}

entity "Grievance" as grievances {
  *id : Integer
  --
  title : String
  category : String
  submitted_by : Integer <<FK>>
  assigned_to : Integer <<FK>>
  status : String
}

entity "Internship" as internships {
  *id : Integer
  --
  title : String
  company : String
  posted_by : Integer <<FK>>
}

entity "Application" as internship_apps {
  *id : Integer
  --
  student_id : Integer <<FK>>
  internship_id : Integer <<FK>>
  status : String
}

entity "Incident" as incidents {
  *id : Integer
  --
  user_id : Integer <<FK>>
  description : String
  status : String
}

' Relationships
users ||..o{ announcements : "posts"
users ||..o{ attendance : "has attendance"
users ||..o{ enrollments : "enrolls in"
users ||..o{ club_members : "joins"
users ||..o{ grievances : "submits"
users ||..o{ incidents : "reports"
users ||..o{ internship_apps : "applies"

courses ||..o{ attendance : "has"
courses ||..o{ enrollments : "has students"

clubs ||..o{ club_members : "has members"

internships ||..o{ internship_apps : "receives"

grievances }o..o{ users : "assigned to"
courses }o..|| users : "taught by"
clubs }o..|| users : "led by"

@enduml
```

## 3. Class Diagram (PlantUML)

Representation of the core backend classes.

```plantuml
@startuml
class User {
  +id: int
  +email: str
  +role: str
  +department: str
}

class Course {
  +id: int
  +name: str
  +code: str
  +credits: int
}

class Grievance {
  +id: int
  +title: str
  +status: str
  +priority: str
}

class Internship {
  +id: int
  +company: str
  +role_type: str
}

class Club {
  +id: int
  +name: str
  +category: str
}

User "1" -- "*" Grievance : creates
User "1" -- "*" Course : enrolls
User "1" -- "*" Club : approaches
User "1" -- "*" Internship : applies
@enduml
```

## 4. Sequence Diagram (PlantUML)

Example flow: User submitting a grievance.

```plantuml
@startuml
actor User
participant "Frontend UI" as UI
participant "API Gateway" as API
participant "Grievance Service" as Service
participant "Database" as DB

User -> UI: Fills Grievance Form
UI -> API: POST /api/grievances
API -> Service: create_grievance(data, user_id)
Service -> DB: Insert new Grievance record
DB --> Service: Return Grievance ID
Service --> API: Return Success Object
API --> UI: 201 Created
UI --> User: Show "Grievance Submitted" Toast
@enduml
```
