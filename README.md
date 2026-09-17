# 🏫 NQU Academic Information System (金門大學校務管理系統)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Storage](<https://img.shields.io/badge/persistence-Big%20Pickle%20(Binary)-orange.svg>)](https://docs.python.org/3/library/pickle.html)
[![Architecture](https://img.shields.io/badge/OOP-Inheritance%20%26%20Polymorphism-success.svg)](#object-oriented-architecture)
[![License](https://img.shields.io/badge/license-Academic%20Evaluation%20Only-lightgrey.svg)](#)

A modular, terminal-based academic management system modeling the core workflow of the National Quemoy University (NQU) Academic Portal. Built as a software engineering homework project (`習題 2`), this application demonstrates robust Object-Oriented Programming (OOP) design patterns, serialized binary data persistence via Python's native `pickle` module ("Big Pickle"), interactive terminal UI elements, and a dynamic student GPA and course evaluation engine.

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Highlights & Architectural Pillars](#-key-highlights--architectural-pillars)
3. [System Architecture & OOP Hierarchy](#-system-architecture--oop-hierarchy)
4. [Data Persistence Engine ("The Big Pickle")](#-data-persistence-engine-the-big-pickle)
5. [Feature Breakdown](#-feature-breakdown)
6. [Directory Structure](#-directory-structure)
7. [Getting Started & Installation](#-getting-started--installation)
8. [Usage Guide & Walkthrough](#-usage-guide--walkthrough)
9. [Error Handling & Edge Cases](#-error-handling--edge-cases)
10. [Future Roadmap & Extensions](#-future-roadmap--extensions)

---

## 📌 Project Overview

University administrative portals must coordinate disparate yet interconnected entities: matriculating students, academic faculty, course catalogs, grade tracking, and real-time persistence.

This project re-engineers those interactions into a streamlined command-line portal. Built to fulfill the academic requirements of **Homework 2 (`習題 2 : 請做一個類似金門大學校務系統的專案程式 (可用 AI, opencode + big pickle) #2`)**, the program serves as a self-contained runtime environment capable of managing students, assigning faculty members to courses, tracking GPA across variable course loads, and serializing the complete system graph to disk in a binary stream.

---

## 🌟 Key Highlights & Architectural Pillars

- **Pure Object-Oriented Design**: Utilizes an abstract/base hierarchy (`Person` → `Student`, `Teacher`) enforcing inheritance, encapsulation, and clear responsibility segregation.
- **State Serialization ("Big Pickle")**: Unlike superficial in-memory scripts that lose state upon exit, this system dumps and unpickles complex object dictionaries preserving identity, references, and nested attributes across runtime sessions.
- **Auto-Bootstrapping Seed Data**: If launched in a completely clean environment without an existing pickle binary, the system automatically bootstraps an NQU CSIE environment (courses, professors, and initial student profiles) so evaluators can test features immediately.
- **Real-Time GPA Engine**: Grades are evaluated dynamically on a 0–100 scale, allowing students to check their running Grade Point Average without manual recalculations.
- **Styled Terminal UX**: ANSI escape styling (`Colors` enum) provides contextual terminal alerts, readable hierarchy headers, and distinctive visual statuses.

---

## 🏛 System Architecture & OOP Hierarchy

The codebase adheres strictly to object-oriented paradigms. By encapsulating data mutations within respective class definitions, business logic remains decoupled from the terminal I/O handler.

```text
       +------------------------------------+
       |              Person                |  <-- Base Class
       +------------------------------------+
       | - user_id: str                     |
       | - name: str                        |
       | - department: str                  |
       +------------------------------------+
                 ^                 ^
                 | (inherits)      | (inherits)
                 |                 |
+--------------------------+     +-------------------------------+
|         Student          |     |            Teacher            |
+--------------------------+     +-------------------------------+
| - enrollments: dict      |     | - title: str                  |
| + enroll(course_id)      |     | - teaching_courses: list      |
| + drop(course_id)        |     | + assign_course(course_id)    |
| + assign_grade(cid, gr)  |     +-------------------------------+
| + calculate_gpa()        |
+--------------------------+

+------------------------------------+     +-------------------------------+
|              Course                |     |           NQUSystem           |  <-- Engine / State Controller
+------------------------------------+     +-------------------------------+
| - course_id: str                   |     | - name: str                        |
| - credits: int                     |     | - teachers: dict[id, Teacher] |
| - teacher_id: str                  |     | - courses: dict[id, Course]   |
+------------------------------------+     | + save_data()                 |
                                           | + load_data()                 |
                                           | + _seed_data()                |
                                           | + display_dashboard()         |
                                           +-------------------------------+
```

### Class Responsibilities:

1. **`Person`**: Base class encapsulating shared identification metadata (`user_id`, `name`, `department`).
2. **`Student`**: Subclass managing student-specific attributes, dictionary-backed course enrollments (`{course_id: grade}`), course addition/dropping, and arithmetic GPA aggregation.
3. **`Teacher`**: Subclass tracking faculty titles (e.g., Associate Professor) and pedagogical responsibilities (`teaching_courses`).
4. **`Course`**: Encapsulates course code definitions, syllabus credit weighting, and assigned instructor identifiers.
5. **`NQUSystem`**: The orchestrator. Manages collection lifecycle, runs the menu loop, mediates input validation, and coordinates serialization/deserialization.

---

## 🥒 Data Persistence Engine ("The Big Pickle")

At the heart of the project requirement is the **"Big Pickle"** pattern. Rather than relying on rigid tabular CSVs or heavyweight external SQL servers, the system leverages Python's high-efficiency binary protocol `pickle`.

### How It Works:

```python
# Serialization pipeline
system_state = {
    'students': self.students,
    'teachers': self.teachers,
    'courses': self.courses
}
with open("nqu_big_pickle.pkl", "wb") as f:
    pickle.dump(system_state, f)
```

1. **State Aggregation**: Whenever a destructive or additive modification occurs (e.g., student registered, grade inputted, course enrolled), all runtime references are collected in an overarching dictionary.
2. **Binary Serializer**: `pickle.dump()` traverses the entire object graph, preserving class types, instance attributes, and cross-references (such as a student holding course IDs linked to catalog courses).
3. **Cold Starts**: Upon system execution, `os.path.exists()` checks for the presence of `nqu_big_pickle.pkl`. If found, the binary stream is reconstituted back into live objects via `pickle.load()`. If not found, `_seed_data()` triggers automatic initialization.

---

## 🚀 Feature Breakdown

| Feature Module            | Method / Mechanism          | Description                                                                                                                                                         |
| :------------------------ | :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **System Dashboard**      | `display_dashboard()`       | Displays a multi-column visual roster of registered faculty, course catalogs with credits/instructors, and all enrolled students with their current grades and GPA. |
| **Student Registration**  | `register_student()`        | Verifies primary key uniqueness (Student ID), prompts for student name and academic department, initializes the object, and writes to pickle.                       |
| **Curriculum Creation**   | `add_course()`              | Adds new course definitions with validation on credit values (handling invalid non-integer inputs gracefully).                                                      |
| **Enrollment Management** | `enroll_and_grade()`        | Multi-action submenu: Enroll a student into a valid course code, drop an existing course, or record an academic score (0–100 scale).                                |
| **GPA Computation**       | `Student.calculate_gpa()`   | Parses all active numerical grades under the student's enrollment record and calculates an accurate mean average in real-time.                                      |
| **Crash Protection**      | `try / except (ValueError)` | Prevents crashes during runtime when non-numeric values are passed to credit or grade prompts.                                                                      |

---

## 📁 Directory Structure

```text
nqu-academic-system/
├── README.md               # Comprehensive system documentation and specs
├── nqu_system.py           # Main executable source code
└── nqu_big_pickle.pkl      # Binary database generated automatically on first run
```

---

## 🛠 Getting Started & Installation

### Prerequisites

- Python 3.8, 3.9, 3.10, 3.11, or newer.
- No external 3rd-party dependencies or pip packages required (uses standard library `pickle`, `os`, and ANSI terminal output).

### Step-by-Step Setup

1. **Clone or Download the Repository:**

   ```bash
   git clone <your-repo-url>
   cd nqu-academic-system
   ```

2. **Verify Python Installation:**

   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Launch the Application:**
   ```bash
   python nqu_system.py
   ```

---

## 🖥 Usage Guide & Walkthrough

Upon executing the script, the main menu loads:

```text
=== NQU Terminal Gateway ===
1. 📊 View University Dashboard
2. 🎓 Register New Student
3. 📚 Create New Course
4. 📝 Manage Enrollments & Grades
5. 🚪 Save & Exit
Select module (1-5):
```

### Scenario Walkthrough: Adding and Grading a Student

1. **Option 2 (Register Student)**:
   - Input Student ID: `112002`
   - Input Student Name: `Alex Chen`
   - Input Department: `CSIE`
   - _Result_: Student instance created, and database state serialized to pickle.

2. **Option 4 (Manage Enrollments & Grades)**:
   - Provide Student ID: `112002`
   - Sub-action: Select `1` (Enroll)
   - Input Course ID: `CSIE201`
   - Sub-action: Select `2` (Assign a grade)
   - Input Grade: `92.5`
   - _Result_: Student `112002` is recorded with 92.5 in `CSIE201`.

3. **Option 1 (View Dashboard)**:
   - View updated statistics. The dashboard reflects the student, enrolled courses, and calculated GPA (`92.50`).

4. **Option 5 (Save & Exit)**:
   - Gracefully synchronizes all objects into `nqu_big_pickle.pkl` and exits without data leakage.

---

## 🛡 Error Handling & Edge Cases

The application handles common real-world user mistakes:

- **Duplicate Identifiers**: Re-registering an existing student ID or course ID prompts a localized warning without overwriting existing data.
- **Non-Existent Keys**: Attempting to enroll a student in an unlisted course or grading an un-enrolled course is rejected cleanly with an explanatory notice.
- **Type Mismatches**: Entering characters when prompted for grades or credit values triggers a `ValueError` block instead of throwing an unhandled exception to the terminal.
- **Zero-Grade GPA Calculations**: Students with no grades registered yield a default `0.00` GPA rather than raising a `ZeroDivisionError`.

---

## 🔮 Future Roadmap & Extensions

While this project fully covers the requirements for Homework 2, modular design allows for straightforward expansion:

- [ ] **Authentication Layer**: Role-based access control separating Student and Admin privileges with password hashing (`hashlib`).
- [ ] **Prerequisite Checking**: Enforcing prerequisite completion before enrollment into 300/400-level CSIE courses.
- [ ] **Data Export Options**: Implementing a JSON/CSV exporter method alongside the binary pickle storage for interoperability.
- [ ] **GUI/Web Frontend**: Connecting the underlying `NQUSystem` controller to a Flask API or Tkinter window.

---

## 👨‍💻 Author & Academic Attribution

- **Course**: Software Engineering / Computer Science & Information Engineering
- **Assignment**: Homework 2 (`習題 2 - 金門大學校務系統`)
- **Institution**: National Quemoy University (國立金門大學 NQU)
