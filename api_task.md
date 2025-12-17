# API Implementation Tasks - PSC Web Django

## Overview
This document outlines all the REST API endpoints that need to be implemented for the PSC Web application. Each endpoint includes the HTTP method, expected input/output data structures, status codes, filters, search capabilities, and pagination requirements.

---

## 1. Students Module

### 1.1 Student Management

#### GET /students/
**Description:** List all students with pagination and filtering
**Pagination:** Yes (page_size=20)
**Filters:**
- `status` (a/i/s/g/w)
- `gender` (m/f/o)
- `date_joined` (date range)
**Search:** `first_name`, `last_name`, `phone_number`
**Response:** 200 OK
```json
{
  "count": 150,
  "next": "http://api/students/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 5,
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "2000-01-15",
      "gender": "m",
      "phone_number": "1234567890",
      "emergency_contact_person_name": "Jane Doe",
      "emergency_contact_number": "0987654321",
      "status": "a",
      "profile_picture": "pic.jpg",
      "date_joined": "2024-09-01",
      "created_date": "2024-08-20T10:00:00Z",
      "updated_date": "2024-08-20T10:00:00Z"
    }
  ]
}
```

#### POST /students/
**Description:** Create a new student
**Request Body:**
```json
{
  "user": 5,
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "2000-01-15",
  "gender": "m",
  "phone_number": "1234567890",
  "emergency_contact_person_name": "Jane Doe",
  "emergency_contact_number": "0987654321",
  "status": "a",
  "profile_picture": "pic.jpg",
  "date_joined": "2024-09-01"
}
```
**Response:** 201 Created
```json
{
  "id": 1,
  "user": 5,
  "first_name": "John",
  "last_name": "Doe",
  ...
}
```
**Error Response:** 400 Bad Request
```json
{
  "phone_number": ["student with this phone number already exists."],
  "user": ["This field is required."]
}
```

#### GET /students/{id}/
**Description:** Retrieve a single student by ID
**Response:** 200 OK (same structure as POST response)
**Error Response:** 404 Not Found
```json
{
  "detail": "Not found."
}
```

#### PUT /students/{id}/
**Description:** Update a student (full update)
**Request Body:** Same as POST
**Response:** 200 OK
**Error Response:** 400 Bad Request, 404 Not Found

#### PATCH /students/{id}/
**Description:** Partial update of a student
**Request Body:** Any subset of student fields
**Response:** 200 OK
**Error Response:** 400 Bad Request, 404 Not Found

#### DELETE /students/{id}/
**Description:** Soft delete a student (sets status to 'i')
**Response:** 204 No Content
**Error Response:** 404 Not Found

### 1.2 Student Nested Endpoints

#### GET /students/with-courses/
**Description:** Get all students with their enrolled courses (minimal fields)
**Pagination:** Yes (page_size=20)
**Filters:** `status`, `course_status`
**Response:** 200 OK
```json
{
  "count": 150,
  "next": "http://api/students/with-courses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "status": "a",
      "courses": [
        {
          "id": 5,
          "title": "Introduction to Python",
          "status": "p"
        },
        {
          "id": 8,
          "title": "Web Development Basics",
          "status": "p"
        }
      ]
    }
  ]
}
```

#### GET /students/{id}/courses/
**Description:** Get all courses for a specific student
**Pagination:** No
**Response:** 200 OK
```json
[
  {
    "id": 5,
    "title": "Introduction to Python",
    "description": "Learn Python programming from scratch",
    "status": "p",
    "enrollment": {
      "id": 12,
      "enrollment_date": "2024-09-01T10:00:00Z",
      "status": "a"
    }
  }
]
```

#### GET /students/{id}/assignments/
**Description:** Get all assignments for a student across all enrolled courses
**Pagination:** Yes (page_size=15)
**Filters:** `course`, `status`, `due_date`
**Response:** 200 OK
```json
{
  "count": 45,
  "next": "http://api/students/{id}/assignments/?page=2",
  "previous": null,
  "results": [
    {
      "id": 10,
      "title": "Python Basics Assignment",
      "course": {
        "id": 5,
        "title": "Introduction to Python"
      },
      "due_date": "2024-10-15T23:59:59Z",
      "submission": {
        "id": 25,
        "status": "g",
        "submitted_date": "2024-10-10T14:30:00Z",
        "grade": {
          "grade": 85.50,
          "feedback": "Good work!"
        }
      }
    }
  ]
}
```

#### GET /students/{id}/exams/
**Description:** Get all exams for a student
**Pagination:** Yes (page_size=10)
**Filters:** `course`, `start_time`, `end_time`
**Response:** 200 OK
```json
{
  "count": 8,
  "results": [
    {
      "id": 3,
      "title": "Python Midterm Exam",
      "course": {
        "id": 5,
        "title": "Introduction to Python"
      },
      "start_time": "2024-10-20T10:00:00Z",
      "end_time": "2024-10-20T12:00:00Z",
      "duration": "02:00:00",
      "total_marks": 100,
      "submission": {
        "id": 15,
        "submitted_at": "2024-10-20T11:45:00Z",
        "review": {
          "score": 87.50,
          "feedback": "Excellent performance"
        }
      }
    }
  ]
}
```

### 1.3 Enrollment Management

#### GET /enrollments/
**Description:** List all enrollments
**Pagination:** Yes (page_size=50)
**Filters:** `student`, `course`, `status`, `enrollment_date`
**Search:** `student__first_name`, `student__last_name`, `course__title`
**Response:** 200 OK
```json
{
  "count": 500,
  "results": [
    {
      "id": 1,
      "student": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe"
      },
      "course": {
        "id": 5,
        "title": "Introduction to Python"
      },
      "enrollment_date": "2024-09-01T10:00:00Z",
      "status": "a"
    }
  ]
}
```

#### POST /enrollments/
**Description:** Enroll a student in a course
**Request Body:**
```json
{
  "student": 1,
  "course": 5,
  "status": "a"
}
```
**Response:** 201 Created
**Error Response:** 400 Bad Request
```json
{
  "detail": "Student is already enrolled in this course."
}
```

#### GET /enrollments/{id}/
**Description:** Get enrollment details
**Response:** 200 OK

#### PATCH /enrollments/{id}/
**Description:** Update enrollment status
**Request Body:**
```json
{
  "status": "c"
}
```
**Response:** 200 OK

#### DELETE /enrollments/{id}/
**Description:** Soft delete enrollment
**Response:** 204 No Content

---

## 2. Course Module

### 2.1 Course Management

#### GET /courses/
**Description:** List all courses
**Pagination:** Yes (page_size=20)
**Filters:** `status` (d/p/a), `created_date`
**Search:** `title`, `description`
**Response:** 200 OK
```json
{
  "count": 50,
  "results": [
    {
      "id": 5,
      "title": "Introduction to Python",
      "description": "Learn Python programming from scratch",
      "status": "p",
      "created_by": 2,
      "updated_by": 2,
      "created_date": "2024-08-01T10:00:00Z",
      "updated_date": "2024-08-15T14:00:00Z"
    }
  ]
}
```

#### POST /courses/
**Description:** Create a new course
**Request Body:**
```json
{
  "title": "Introduction to Python",
  "description": "Learn Python programming from scratch",
  "status": "d"
}
```
**Response:** 201 Created
**Error Response:** 400 Bad Request

#### GET /courses/{id}/
**Description:** Get course details
**Response:** 200 OK

#### PUT /courses/{id}/
**Description:** Full update of course
**Response:** 200 OK

#### PATCH /courses/{id}/
**Description:** Partial update of course
**Response:** 200 OK

#### DELETE /courses/{id}/
**Description:** Delete course
**Response:** 204 No Content

### 2.2 Course Nested Endpoints

#### GET /courses/{id}/students/
**Description:** Get all students enrolled in a course
**Pagination:** Yes (page_size=30)
**Filters:** `enrollment_status`, `student_status`
**Search:** `first_name`, `last_name`
**Response:** 200 OK
```json
{
  "count": 45,
  "results": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "phone_number": "1234567890",
      "status": "a",
      "enrollment": {
        "id": 12,
        "enrollment_date": "2024-09-01T10:00:00Z",
        "status": "a"
      }
    }
  ]
}
```

#### GET /courses/{id}/teachers/
**Description:** Get all teachers assigned to a course
**Pagination:** No
**Response:** 200 OK
```json
[
  {
    "id": 3,
    "teacher": {
      "id": 2,
      "first_name": "Jane",
      "last_name": "Smith",
      "employee_code": "EMP001",
      "email_institutional": "jane.smith@psc.edu"
    },
    "status": "a",
    "created_date": "2024-08-15T10:00:00Z"
  }
]
```

#### POST /courses/{id}/teachers/
**Description:** Assign a teacher to a course
**Request Body:**
```json
{
  "teacher": 2,
  "status": "a"
}
```
**Response:** 201 Created
**Error Response:** 400 Bad Request

#### GET /courses/{id}/materials/
**Description:** Get all materials for a course
**Pagination:** Yes (page_size=20)
**Filters:** `type` (document/video/link/slides), `status`, `upload_date`
**Search:** `title`, `description`
**Response:** 200 OK
```json
{
  "count": 25,
  "results": [
    {
      "id": 8,
      "title": "Week 1 - Introduction Slides",
      "description": "Introduction to course concepts",
      "file_url": "https://example.com/materials/week1.pdf",
      "upload_date": "2024-09-01T08:00:00Z",
      "type": "slides",
      "status": "a",
      "teacher": {
        "id": 2,
        "first_name": "Jane",
        "last_name": "Smith"
      }
    }
  ]
}
```

#### POST /courses/{id}/materials/
**Description:** Add material to a course
**Request Body:**
```json
{
  "title": "Week 1 - Introduction Slides",
  "description": "Introduction to course concepts",
  "file_url": "https://example.com/materials/week1.pdf",
  "type": "slides",
  "status": "a",
  "teacher": 2
}
```
**Response:** 201 Created

#### GET /courses/{id}/assignments/
**Description:** Get all assignments for a course
**Pagination:** Yes (page_size=15)
**Filters:** `due_date`, `teacher`
**Response:** 200 OK
```json
{
  "count": 10,
  "results": [
    {
      "id": 5,
      "title": "Python Basics Assignment",
      "description": "Complete exercises 1-10",
      "due_date": "2024-10-15T23:59:59Z",
      "teacher": {
        "id": 2,
        "first_name": "Jane",
        "last_name": "Smith"
      },
      "created_date": "2024-09-20T10:00:00Z"
    }
  ]
}
```

#### POST /courses/{id}/assignments/
**Description:** Create assignment for a course
**Request Body:**
```json
{
  "title": "Python Basics Assignment",
  "description": "Complete exercises 1-10",
  "due_date": "2024-10-15T23:59:59Z",
  "teacher": 2
}
```
**Response:** 201 Created

#### GET /courses/{id}/exams/
**Description:** Get all exams for a course
**Pagination:** Yes (page_size=10)
**Filters:** `start_time`, `end_time`
**Response:** 200 OK
```json
{
  "count": 4,
  "results": [
    {
      "id": 1,
      "title": "Python Midterm Exam",
      "description": "Covers chapters 1-5",
      "duration": "02:00:00",
      "start_time": "2024-10-20T10:00:00Z",
      "end_time": "2024-10-20T12:00:00Z",
      "total_marks": 100,
      "question_count": 25
    }
  ]
}
```

#### GET /courses/with-stats/
**Description:** Get all courses with enrollment statistics
**Pagination:** Yes (page_size=15)
**Filters:** `status`
**Response:** 200 OK
```json
{
  "count": 50,
  "results": [
    {
      "id": 5,
      "title": "Introduction to Python",
      "status": "p",
      "total_students": 45,
      "active_students": 42,
      "total_teachers": 2,
      "total_materials": 25,
      "total_assignments": 10
    }
  ]
}
```

### 2.3 Material Management

#### GET /materials/
**Description:** List all materials
**Pagination:** Yes (page_size=30)
**Filters:** `course`, `type`, `status`, `teacher`, `upload_date`
**Search:** `title`, `description`
**Response:** 200 OK

#### POST /materials/
**Description:** Create a new material
**Response:** 201 Created

#### GET /materials/{id}/
**Description:** Get material details
**Response:** 200 OK

#### PATCH /materials/{id}/
**Description:** Update material
**Response:** 200 OK

#### DELETE /materials/{id}/
**Description:** Delete material
**Response:** 204 No Content

### 2.4 Course Teacher Management

#### GET /course-teachers/
**Description:** List all course-teacher assignments
**Pagination:** Yes (page_size=50)
**Filters:** `course`, `teacher`, `status`
**Response:** 200 OK

#### DELETE /course-teachers/{id}/
**Description:** Remove teacher from course
**Response:** 204 No Content

---

## 3. Staff Module

### 3.1 Teacher Management

#### GET /teachers/
**Description:** List all teachers
**Pagination:** Yes (page_size=20)
**Filters:** `status` (a/i/l/r/t), `gender`, `experience_years`, `date_joined`
**Search:** `first_name`, `last_name`, `employee_code`, `email_institutional`
**Response:** 200 OK
```json
{
  "count": 30,
  "results": [
    {
      "id": 2,
      "user": 10,
      "first_name": "Jane",
      "last_name": "Smith",
      "dob": "1985-05-20",
      "gender": "f",
      "employee_code": "EMP001",
      "experience_years": 8,
      "phone_number": "9876543210",
      "emergency_contact_number": "1234567890",
      "email_institutional": "jane.smith@psc.edu",
      "status": "a",
      "profile_picture": "profile.jpg",
      "date_joined": "2020-08-15T10:00:00Z"
    }
  ]
}
```

#### POST /teachers/
**Description:** Create a new teacher
**Request Body:**
```json
{
  "user": 10,
  "first_name": "Jane",
  "last_name": "Smith",
  "dob": "1985-05-20",
  "gender": "f",
  "employee_code": "EMP001",
  "experience_years": 8,
  "phone_number": "9876543210",
  "emergency_contact_number": "1234567890",
  "email_institutional": "jane.smith@psc.edu",
  "status": "a",
  "date_joined": "2020-08-15"
}
```
**Response:** 201 Created
**Error Response:** 400 Bad Request
```json
{
  "employee_code": ["teacher with this employee code already exists."],
  "email_institutional": ["teacher with this email institutional already exists."]
}
```

#### GET /teachers/{id}/
**Description:** Get teacher details
**Response:** 200 OK

#### PATCH /teachers/{id}/
**Description:** Update teacher
**Response:** 200 OK

#### DELETE /teachers/{id}/
**Description:** Soft delete teacher
**Response:** 204 No Content

### 3.2 Teacher Nested Endpoints

#### GET /teachers/{id}/courses/
**Description:** Get all courses assigned to a teacher
**Pagination:** Yes (page_size=20)
**Filters:** `status`
**Response:** 200 OK
```json
{
  "count": 5,
  "results": [
    {
      "id": 5,
      "title": "Introduction to Python",
      "description": "Learn Python programming",
      "status": "p",
      "assignment": {
        "id": 8,
        "status": "a",
        "created_date": "2024-08-15T10:00:00Z"
      },
      "student_count": 45
    }
  ]
}
```

#### GET /teachers/{id}/materials/
**Description:** Get all materials uploaded by a teacher
**Pagination:** Yes (page_size=25)
**Filters:** `course`, `type`, `status`
**Response:** 200 OK

#### GET /teachers/{id}/assignments/
**Description:** Get all assignments created by a teacher
**Pagination:** Yes (page_size=20)
**Filters:** `course`, `due_date`
**Response:** 200 OK

#### GET /teachers/with-workload/
**Description:** Get all teachers with workload statistics
**Pagination:** Yes (page_size=20)
**Filters:** `status`
**Response:** 200 OK
```json
{
  "count": 30,
  "results": [
    {
      "id": 2,
      "first_name": "Jane",
      "last_name": "Smith",
      "employee_code": "EMP001",
      "status": "a",
      "total_courses": 5,
      "total_students": 185,
      "total_assignments": 25,
      "pending_submissions": 42
    }
  ]
}
```

### 3.3 Department Management

#### GET /departments/
**Description:** List all departments
**Pagination:** Yes (page_size=30)
**Filters:** `status`
**Search:** `name`, `description`
**Response:** 200 OK
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "name": "Computer Science",
      "description": "CS Department",
      "status": "a",
      "created_date": "2024-01-01T10:00:00Z"
    }
  ]
}
```

#### POST /departments/
**Description:** Create a new department
**Request Body:**
```json
{
  "name": "Computer Science",
  "description": "CS Department",
  "status": "a"
}
```
**Response:** 201 Created

#### GET /departments/{id}/
**Description:** Get department details
**Response:** 200 OK

#### GET /departments/{id}/teachers/
**Description:** Get all teachers in a department
**Pagination:** Yes (page_size=30)
**Response:** 200 OK

#### POST /departments/{id}/teachers/
**Description:** Assign teacher to department (via UserDepartment)
**Request Body:**
```json
{
  "user": 10,
  "status": "a"
}
```
**Response:** 201 Created

### 3.4 Qualification Management

#### GET /qualifications/
**Description:** List all qualifications
**Pagination:** Yes (page_size=20)
**Filters:** `status`
**Search:** `name`
**Response:** 200 OK
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "name": "Ph.D. in Computer Science",
      "description": "Doctoral degree",
      "status": "a"
    }
  ]
}
```

#### POST /qualifications/
**Request Body:**
```json
{
  "name": "Ph.D. in Computer Science",
  "description": "Doctoral degree",
  "status": "a"
}
```
**Response:** 201 Created

#### GET /user-qualifications/
**Description:** List all user-qualification mappings
**Pagination:** Yes (page_size=50)
**Filters:** `user`, `qualification`, `status`
**Response:** 200 OK

#### POST /user-qualifications/
**Description:** Assign qualification to user
**Request Body:**
```json
{
  "user": 10,
  "qualification": 1,
  "status": "a"
}
```
**Response:** 201 Created

### 3.5 Specialization Management

#### GET /specializations/
**Description:** List all specializations
**Pagination:** Yes (page_size=20)
**Filters:** `status`
**Search:** `name`
**Response:** 200 OK

#### POST /specializations/
**Request Body:**
```json
{
  "name": "Machine Learning",
  "description": "ML specialization",
  "status": "a"
}
```
**Response:** 201 Created

#### GET /user-specializations/
**Description:** List all user-specialization mappings
**Pagination:** Yes (page_size=50)
**Filters:** `user`, `specialization`, `status`
**Response:** 200 OK

#### POST /user-specializations/
**Description:** Assign specialization to user
**Request Body:**
```json
{
  "user": 10,
  "specialization": 2,
  "status": "a"
}
```
**Response:** 201 Created

### 3.6 Designation Management

#### GET /designations/
**Description:** List all designations
**Pagination:** Yes (page_size=20)
**Filters:** `status`
**Search:** `designation_name`
**Response:** 200 OK

#### POST /designations/
**Request Body:**
```json
{
  "designation_name": "Assistant Professor",
  "description": "Entry level teaching position",
  "status": "a"
}
```
**Response:** 201 Created

#### GET /user-designations/
**Description:** List all user-designation mappings
**Pagination:** Yes (page_size=50)
**Filters:** `user`, `designation`, `status`
**Response:** 200 OK

---

## 4. Assessment Module

### 4.1 Assignment Management

#### GET /assignments/
**Description:** List all assignments
**Pagination:** Yes (page_size=25)
**Filters:** `course`, `teacher`, `due_date`, `created_date`
**Search:** `title`, `description`
**Response:** 200 OK
```json
{
  "count": 100,
  "results": [
    {
      "id": 5,
      "course": {
        "id": 5,
        "title": "Introduction to Python"
      },
      "teacher": {
        "id": 2,
        "first_name": "Jane",
        "last_name": "Smith"
      },
      "title": "Python Basics Assignment",
      "description": "Complete exercises 1-10",
      "due_date": "2024-10-15T23:59:59Z",
      "created_date": "2024-09-20T10:00:00Z"
    }
  ]
}
```

#### POST /assignments/
**Description:** Create a new assignment
**Request Body:**
```json
{
  "course": 5,
  "teacher": 2,
  "title": "Python Basics Assignment",
  "description": "Complete exercises 1-10",
  "due_date": "2024-10-15T23:59:59Z"
}
```
**Response:** 201 Created

#### GET /assignments/{id}/
**Description:** Get assignment details
**Response:** 200 OK

#### PATCH /assignments/{id}/
**Description:** Update assignment
**Response:** 200 OK

#### DELETE /assignments/{id}/
**Description:** Delete assignment
**Response:** 204 No Content

### 4.2 Assignment Nested Endpoints

#### GET /assignments/{id}/submissions/
**Description:** Get all submissions for an assignment
**Pagination:** Yes (page_size=30)
**Filters:** `status` (s/l/g), `submitted_date`
**Search:** `student__first_name`, `student__last_name`
**Response:** 200 OK
```json
{
  "count": 42,
  "results": [
    {
      "id": 25,
      "student": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe"
      },
      "file_url": "https://example.com/submissions/file.pdf",
      "submitted_date": "2024-10-10T14:30:00Z",
      "status": "g",
      "grade": {
        "id": 15,
        "grade": 85.50,
        "graded_by": {
          "id": 2,
          "first_name": "Jane",
          "last_name": "Smith"
        },
        "feedback": "Good work!"
      }
    }
  ]
}
```

#### GET /assignments/{id}/submissions/pending/
**Description:** Get pending (ungraded) submissions
**Pagination:** Yes (page_size=30)
**Response:** 200 OK

### 4.3 Submission Management

#### GET /submissions/
**Description:** List all submissions
**Pagination:** Yes (page_size=30)
**Filters:** `assignment`, `student`, `status`, `submitted_date`
**Response:** 200 OK

#### POST /submissions/
**Description:** Submit an assignment (student action)
**Request Body:**
```json
{
  "assignment": 5,
  "student": 1,
  "file_url": "https://example.com/submissions/file.pdf",
  "status": "s"
}
```
**Response:** 201 Created
**Error Response:** 400 Bad Request
```json
{
  "detail": "Submission deadline has passed."
}
```

#### GET /submissions/{id}/
**Description:** Get submission details
**Response:** 200 OK

#### PATCH /submissions/{id}/
**Description:** Update submission (before grading)
**Response:** 200 OK

#### DELETE /submissions/{id}/
**Description:** Delete submission
**Response:** 204 No Content

### 4.4 Submission Grade Management

#### GET /submission-grades/
**Description:** List all grades
**Pagination:** Yes (page_size=50)
**Filters:** `submission`, `graded_by`, `created_date`
**Response:** 200 OK

#### POST /submission-grades/
**Description:** Grade a submission (teacher action)
**Request Body:**
```json
{
  "submission": 25,
  "grade": 85.50,
  "graded_by": 2,
  "feedback": "Good work! Keep it up."
}
```
**Response:** 201 Created

#### GET /submission-grades/{id}/
**Description:** Get grade details
**Response:** 200 OK

#### PATCH /submission-grades/{id}/
**Description:** Update grade
**Response:** 200 OK

### 4.5 Exam Management

#### GET /exams/
**Description:** List all exams
**Pagination:** Yes (page_size=20)
**Filters:** `course`, `start_time`, `end_time`
**Search:** `title`, `description`
**Response:** 200 OK
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "course": {
        "id": 5,
        "title": "Introduction to Python"
      },
      "title": "Python Midterm Exam",
      "description": "Covers chapters 1-5",
      "duration": "02:00:00",
      "start_time": "2024-10-20T10:00:00Z",
      "end_time": "2024-10-20T12:00:00Z",
      "total_marks": 100
    }
  ]
}
```

#### POST /exams/
**Description:** Create a new exam
**Request Body:**
```json
{
  "course": 5,
  "title": "Python Midterm Exam",
  "description": "Covers chapters 1-5",
  "duration": "02:00:00",
  "start_time": "2024-10-20T10:00:00Z",
  "end_time": "2024-10-20T12:00:00Z",
  "total_marks": 100
}
```
**Response:** 201 Created

#### GET /exams/{id}/
**Description:** Get exam details with questions
**Response:** 200 OK
```json
{
  "id": 1,
  "course": {...},
  "title": "Python Midterm Exam",
  "description": "Covers chapters 1-5",
  "duration": "02:00:00",
  "start_time": "2024-10-20T10:00:00Z",
  "end_time": "2024-10-20T12:00:00Z",
  "total_marks": 100,
  "questions": [
    {
      "id": 10,
      "category": {
        "id": 2,
        "name": "Python Basics"
      },
      "question_text": "What is a variable?",
      "question_type": "s",
      "marks": 4.00,
      "options": [
        {
          "id": 41,
          "option_code": "A",
          "option_text": "A container for data",
          "is_correct": true
        },
        {
          "id": 42,
          "option_code": "B",
          "option_text": "A function",
          "is_correct": false
        }
      ]
    }
  ]
}
```

#### PATCH /exams/{id}/
**Description:** Update exam
**Response:** 200 OK

#### DELETE /exams/{id}/
**Description:** Delete exam
**Response:** 204 No Content

### 4.6 Exam Nested Endpoints

#### GET /exams/{id}/questions/
**Description:** Get all questions for an exam
**Pagination:** No
**Filters:** `category`, `question_type`
**Response:** 200 OK

#### POST /exams/{id}/questions/
**Description:** Add question to exam (creates ExamQuestionMap)
**Request Body:**
```json
{
  "question": 10
}
```
**Response:** 201 Created

#### DELETE /exams/{id}/questions/{question_id}/
**Description:** Remove question from exam
**Response:** 204 No Content

#### GET /exams/{id}/submissions/
**Description:** Get all submissions for an exam
**Pagination:** Yes (page_size=30)
**Filters:** `student`, `submitted_at`
**Response:** 200 OK

### 4.7 Question Management

#### GET /questions/
**Description:** List all exam questions
**Pagination:** Yes (page_size=30)
**Filters:** `category`, `question_type` (s/m/t)
**Search:** `question_text`
**Response:** 200 OK
```json
{
  "count": 200,
  "results": [
    {
      "id": 10,
      "category": {
        "id": 2,
        "name": "Python Basics"
      },
      "question_text": "What is a variable?",
      "question_type": "s",
      "marks": 4.00
    }
  ]
}
```

#### POST /questions/
**Description:** Create a new question
**Request Body:**
```json
{
  "category": 2,
  "question_text": "What is a variable?",
  "question_type": "s",
  "marks": 4.00
}
```
**Response:** 201 Created

#### GET /questions/{id}/
**Description:** Get question details with options
**Response:** 200 OK

#### PATCH /questions/{id}/
**Description:** Update question
**Response:** 200 OK

#### DELETE /questions/{id}/
**Description:** Delete question
**Response:** 204 No Content

### 4.8 Question Options Management

#### GET /question-options/
**Description:** List all question options
**Pagination:** Yes (page_size=100)
**Filters:** `question`, `is_correct`
**Response:** 200 OK

#### POST /question-options/
**Description:** Create option for a question
**Request Body:**
```json
{
  "question": 10,
  "option_code": "A",
  "option_text": "A container for data",
  "is_correct": true
}
```
**Response:** 201 Created

#### PATCH /question-options/{id}/
**Description:** Update option
**Response:** 200 OK

#### DELETE /question-options/{id}/
**Description:** Delete option
**Response:** 204 No Content

### 4.9 Question Categories

#### GET /question-categories/
**Description:** List all question categories
**Pagination:** Yes (page_size=30)
**Search:** `name`
**Response:** 200 OK
```json
{
  "count": 20,
  "results": [
    {
      "id": 2,
      "name": "Python Basics",
      "description": "Basic Python concepts"
    }
  ]
}
```

#### POST /question-categories/
**Request Body:**
```json
{
  "name": "Python Basics",
  "description": "Basic Python concepts"
}
```
**Response:** 201 Created

### 4.10 Exam Submission Management

#### GET /exam-submissions/
**Description:** List all exam submissions
**Pagination:** Yes (page_size=30)
**Filters:** `exam`, `student`, `submitted_at`
**Response:** 200 OK

#### POST /exam-submissions/
**Description:** Submit exam (student action)
**Request Body:**
```json
{
  "exam": 1,
  "student": 1
}
```
**Response:** 201 Created
**Note:** This creates the submission record; answers are submitted separately

#### GET /exam-submissions/{id}/
**Description:** Get exam submission with answers
**Response:** 200 OK
```json
{
  "id": 15,
  "exam": {...},
  "student": {...},
  "submitted_at": "2024-10-20T11:45:00Z",
  "answers": [
    {
      "id": 50,
      "question": {
        "id": 10,
        "question_text": "What is a variable?"
      },
      "answer_text": null,
      "selected_options": [
        {
          "id": 41,
          "option_code": "A",
          "option_text": "A container for data"
        }
      ]
    }
  ],
  "review": {
    "id": 8,
    "score": 87.50,
    "graded_by": {...},
    "feedback": "Excellent performance"
  }
}
```

### 4.11 Exam Answer Management

#### POST /exam-answers/
**Description:** Submit answer to a question (during exam)
**Request Body:**
```json
{
  "exam_submission": 15,
  "question": 10,
  "answer_text": null
}
```
**Response:** 201 Created
**Note:** For multiple choice, create ExamAnswerOption entries separately

#### POST /exam-answer-options/
**Description:** Link selected option to answer
**Request Body:**
```json
{
  "answer": 50,
  "option": 41
}
```
**Response:** 201 Created

### 4.12 Exam Review Management

#### GET /exam-reviews/
**Description:** List all exam reviews
**Pagination:** Yes (page_size=30)
**Filters:** `exam_submission`, `graded_by`
**Response:** 200 OK

#### POST /exam-reviews/
**Description:** Review and grade exam submission
**Request Body:**
```json
{
  "exam_submission": 15,
  "score": 87.50,
  "graded_by": 2,
  "feedback": "Excellent performance on most questions"
}
```
**Response:** 201 Created

#### PATCH /exam-reviews/{id}/
**Description:** Update exam review
**Response:** 200 OK

---

## 5. Communication Module

### 5.1 Chat Management

#### GET /chats/
**Description:** List all chat messages
**Pagination:** Yes (page_size=50)
**Filters:** `course`, `sender`, `timestamp`, `auditory`
**Search:** `message`
**Response:** 200 OK
```json
{
  "count": 500,
  "results": [
    {
      "id": 100,
      "course": {
        "id": 5,
        "title": "Introduction to Python"
      },
      "sender": {
        "id": 1,
        "username": "john.doe",
        "first_name": "John",
        "last_name": "Doe"
      },
      "message": "Can someone explain recursion?",
      "timestamp": "2024-10-15T14:30:00Z",
      "auditory": "all",
      "response_count": 3
    }
  ]
}
```

#### POST /chats/
**Description:** Send a chat message
**Request Body:**
```json
{
  "course": 5,
  "sender": 1,
  "message": "Can someone explain recursion?",
  "auditory": "all"
}
```
**Response:** 201 Created

#### GET /chats/{id}/
**Description:** Get chat message details with responses
**Response:** 200 OK
```json
{
  "id": 100,
  "course": {...},
  "sender": {...},
  "message": "Can someone explain recursion?",
  "timestamp": "2024-10-15T14:30:00Z",
  "auditory": "all",
  "responses": [
    {
      "id": 201,
      "sender": {
        "id": 2,
        "username": "jane.smith",
        "first_name": "Jane",
        "last_name": "Smith"
      },
      "message": "Recursion is when a function calls itself...",
      "timestamp": "2024-10-15T14:35:00Z"
    }
  ]
}
```

#### DELETE /chats/{id}/
**Description:** Delete chat message
**Response:** 204 No Content

### 5.2 Chat Response Management

#### GET /chat-responses/
**Description:** List all chat responses
**Pagination:** Yes (page_size=50)
**Filters:** `chat`, `course`, `sender`, `timestamp`
**Response:** 200 OK

#### POST /chat-responses/
**Description:** Reply to a chat message
**Request Body:**
```json
{
  "course": 5,
  "chat": 100,
  "sender": 2,
  "message": "Recursion is when a function calls itself...",
  "auditory": "all"
}
```
**Response:** 201 Created

#### DELETE /chat-responses/{id}/
**Description:** Delete response
**Response:** 204 No Content

### 5.3 Chat Nested Endpoints

#### GET /courses/{id}/chats/
**Description:** Get all chat messages for a course
**Pagination:** Yes (page_size=50)
**Filters:** `sender`, `timestamp`, `auditory`
**Response:** 200 OK

#### GET /chats/recent/
**Description:** Get recent chat messages across all courses (for user)
**Pagination:** Yes (page_size=30)
**Filters:** `course`
**Response:** 200 OK

---

## 6. Additional Nested and Action Endpoints

### 6.1 Statistics Endpoints

#### GET /dashboard/student/{id}/
**Description:** Get student dashboard statistics
**Response:** 200 OK
```json
{
  "student": {...},
  "enrolled_courses": 5,
  "completed_courses": 2,
  "pending_assignments": 8,
  "upcoming_exams": 3,
  "average_grade": 85.5,
  "recent_activity": [...]
}
```

#### GET /dashboard/teacher/{id}/
**Description:** Get teacher dashboard statistics
**Response:** 200 OK
```json
{
  "teacher": {...},
  "active_courses": 5,
  "total_students": 185,
  "pending_submissions": 42,
  "pending_exam_reviews": 15,
  "upcoming_exams": 2
}
```

#### GET /dashboard/admin/
**Description:** Get admin dashboard statistics
**Response:** 200 OK
```json
{
  "total_students": 500,
  "active_students": 472,
  "total_teachers": 35,
  "active_teachers": 32,
  "total_courses": 50,
  "published_courses": 42,
  "total_enrollments": 2340
}
```

### 6.2 Search Endpoints

#### GET /search/students/?q=john
**Description:** Global student search
**Pagination:** Yes (page_size=20)
**Response:** 200 OK

#### GET /search/teachers/?q=smith
**Description:** Global teacher search
**Pagination:** Yes (page_size=20)
**Response:** 200 OK

#### GET /search/courses/?q=python
**Description:** Global course search
**Pagination:** Yes (page_size=20)
**Response:** 200 OK

### 6.3 Bulk Action Endpoints

#### POST /enrollments/bulk/
**Description:** Bulk enroll students in a course
**Request Body:**
```json
{
  "course": 5,
  "students": [1, 2, 3, 4, 5],
  "status": "a"
}
```
**Response:** 201 Created
```json
{
  "created": 5,
  "failed": 0,
  "details": [...]
}
```

#### POST /submissions/bulk-grade/
**Description:** Bulk grade submissions
**Request Body:**
```json
{
  "grades": [
    {"submission": 1, "grade": 85.5, "feedback": "Good"},
    {"submission": 2, "grade": 90.0, "feedback": "Excellent"}
  ],
  "graded_by": 2
}
```
**Response:** 200 OK

---

## Implementation Guidelines

### Common Response Codes
- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Validation errors
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Pagination Format
All paginated endpoints return:
```json
{
  "count": 150,
  "next": "http://api/endpoint/?page=3",
  "previous": "http://api/endpoint/?page=1",
  "results": [...]
}
```

### Filter Format
Filters are applied via query parameters:
- `/students/?status=a&gender=m`
- `/courses/?status=p&created_date__gte=2024-01-01`
- `/assignments/?due_date__lte=2024-12-31`

### Search Format
Search is applied via `search` query parameter:
- `/students/?search=john`
- `/courses/?search=python`

### Ordering
Use `ordering` parameter:
- `/students/?ordering=first_name`
- `/students/?ordering=-created_date` (descending)

### Common Headers
**Request:**
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Response:**
```
Content-Type: application/json
```

---



*Happy Coding! 🚀*
