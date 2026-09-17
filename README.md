with open("README.md", "w", encoding="utf-8") as f:
f.write("""# 🏫 NQU Academic Information System (金門大學校務管理系統)

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
