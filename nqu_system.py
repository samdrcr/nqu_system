import pickle
import os

# --- ANSI Color Codes for Terminal UI ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- Base Classes (Demonstrating Inheritance) ---
class Person:
    """Base class for people in the NQU system."""
    def __init__(self, user_id: str, name: str, department: str):
        self.user_id = user_id
        self.name = name
        self.department = department

class Teacher(Person):
    """Represents a professor."""
    def __init__(self, user_id: str, name: str, department: str, title: str):
        super().__init__(user_id, name, department)
        self.title = title
        self.teaching_courses = []

    def assign_course(self, course_id: str):
        if course_id not in self.teaching_courses:
            self.teaching_courses.append(course_id)

    def __str__(self):
        return f"[Prof. {self.user_id}] {self.name} - {self.department} ({self.title})"

class Student(Person):
    """Represents a university student with GPA tracking."""
    def __init__(self, user_id: str, name: str, department: str):
        super().__init__(user_id, name, department)
        self.enrollments = {}  # Format: {course_id: grade}

    def enroll(self, course_id: str):
        if course_id not in self.enrollments:
            self.enrollments[course_id] = None  # None means enrolled but not graded yet

    def drop(self, course_id: str):
        if course_id in self.enrollments:
            del self.enrollments[course_id]

    def assign_grade(self, course_id: str, grade: float):
        if course_id in self.enrollments:
            self.enrollments[course_id] = grade

    def calculate_gpa(self):
        grades = [g for g in self.enrollments.values() if g is not None]
        if not grades:
            return 0.0
        return sum(grades) / len(grades)

    def __str__(self):
        gpa = self.calculate_gpa()
        return f"[{self.user_id}] {self.name} ({self.department}) | GPA: {gpa:.2f} | Courses: {len(self.enrollments)}"

class Course:
    """Represents an academic course."""
    def __init__(self, course_id: str, name: str, credits: int):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.teacher_id = None

    def __str__(self):
        prof = f"Assigned to: {self.teacher_id}" if self.teacher_id else "No Professor"
        return f"{Colors.BLUE}[{self.course_id}]{Colors.ENDC} {self.name} ({self.credits} Credits) - {prof}"


# --- Core System Manager ---
class NQUSystem:
    def __init__(self, db_file="nqu_big_pickle.pkl"):
        self.db_file = db_file
        self.students = {}
        self.teachers = {}
        self.courses = {}
        self.load_data()

    def save_data(self):
        """Serializes and saves system data (The Big Pickle)."""
        with open(self.db_file, 'wb') as f:
            pickle.dump({
                'students': self.students, 
                'teachers': self.teachers, 
                'courses': self.courses
            }, f)
        print(f"{Colors.GREEN}💾 System state successfully preserved in big pickle!{Colors.ENDC}")

    def load_data(self):
        """Loads data, or seeds default data if fresh start."""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'rb') as f:
                data = pickle.load(f)
                self.students = data.get('students', {})
                self.teachers = data.get('teachers', {})
                self.courses = data.get('courses', {})
        else:
            print(f"{Colors.WARNING}⚠️ No database found. Generating default NQU CSIE environment...{Colors.ENDC}")
            self._seed_data()

    def _seed_data(self):
        # Seed Courses
        self.courses['CSIE201'] = Course('CSIE201', 'Data Structures & Algorithms', 3)
        self.courses['CSIE302'] = Course('CSIE302', 'Machine Learning Foundations', 3)
        self.courses['CSIE405'] = Course('CSIE405', 'React & TypeScript Web Dev', 3)
        
        # Seed Teachers
        self.teachers['T001'] = Teacher('T001', 'Dr. Lin', 'CSIE', 'Associate Prof')
        self.courses['CSIE201'].teacher_id = 'T001'
        
        # Seed Students (Adding you natively)
        self.students['112001'] = Student('112001', 'Fan Quanrong', 'CSIE')
        self.students['112001'].enroll('CSIE201')
        self.students['112001'].enroll('CSIE405')
        self.save_data()

    # --- Feature Methods ---
    def add_course(self):
        cid = input("Course ID (e.g., CSIE101): ")
        if cid in self.courses:
            print(f"{Colors.FAIL}Course already exists!{Colors.ENDC}")
            return
        name = input("Course Name: ")
        try:
            credits = int(input("Credits: "))
            self.courses[cid] = Course(cid, name, credits)
            print(f"{Colors.GREEN}Course Added!{Colors.ENDC}")
            self.save_data()
        except ValueError:
            print(f"{Colors.FAIL}Credits must be a number!{Colors.ENDC}")

    def register_student(self):
        sid = input("Student ID: ")
        if sid in self.students:
            print(f"{Colors.FAIL}Student already exists!{Colors.ENDC}")
            return
        name = input("Student Name: ")
        dept = input("Department: ")
        self.students[sid] = Student(sid, name, dept)
        print(f"{Colors.GREEN}Student {name} Registered!{Colors.ENDC}")
        self.save_data()

    def enroll_and_grade(self):
        sid = input("Enter Student ID: ")
        if sid not in self.students:
            print(f"{Colors.FAIL}Student not found.{Colors.ENDC}")
            return
            
        print("\n1. Enroll in a course\n2. Assign a grade\n3. Drop a course")
        choice = input("Select action: ")
        
        if choice == '1':
            cid = input("Enter Course ID to enroll: ")
            if cid in self.courses:
                self.students[sid].enroll(cid)
                print(f"{Colors.GREEN}Enrolled successfully.{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}Course not found.{Colors.ENDC}")
        elif choice == '2':
            cid = input("Enter Course ID: ")
            if cid in self.students[sid].enrollments:
                try:
                    grade = float(input("Enter Grade (0-100): "))
                    self.students[sid].assign_grade(cid, grade)
                    print(f"{Colors.GREEN}Grade updated!{Colors.ENDC}")
                except ValueError:
                    print(f"{Colors.FAIL}Invalid grade format.{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}Student is not enrolled in this course.{Colors.ENDC}")
        
        self.save_data()

    def display_dashboard(self):
        print(f"\n{Colors.HEADER}=== 🏫 NQU UNIVERSITY DASHBOARD ==={Colors.ENDC}")
        print(f"\n{Colors.BOLD}--- Faculty ---{Colors.ENDC}")
        for t in self.teachers.values(): print(t)
        
        print(f"\n{Colors.BOLD}--- Course Catalog ---{Colors.ENDC}")
        for c in self.courses.values(): print(c)
        
        print(f"\n{Colors.BOLD}--- Enrolled Students ---{Colors.ENDC}")
        for s in self.students.values(): 
            print(s)
            for cid, grade in s.enrollments.items():
                status = f"Grade: {grade}" if grade is not None else "In Progress"
                print(f"  └─ {cid}: {status}")
        print("-" * 40)

def main():
    system = NQUSystem()
    
    while True:
        print(f"\n{Colors.BOLD}{Colors.BLUE}=== NQU Terminal Gateway ==={Colors.ENDC}")
        print("1. 📊 View University Dashboard")
        print("2. 🎓 Register New Student")
        print("3. 📚 Create New Course")
        print("4. 📝 Manage Enrollments & Grades")
        print("5. 🚪 Save & Exit")
        
        choice = input(f"{Colors.WARNING}Select module (1-5): {Colors.ENDC}")
        
        if choice == '1':
            system.display_dashboard()
        elif choice == '2':
            system.register_student()
        elif choice == '3':
            system.add_course()
        elif choice == '4':
            system.enroll_and_grade()
        elif choice == '5':
            system.save_data()
            print(f"{Colors.GREEN}Session terminated. Have a good day!{Colors.ENDC}")
            break
        else:
            print(f"{Colors.FAIL}Invalid input. Rebooting menu...{Colors.ENDC}")

if __name__ == "__main__":
    main()