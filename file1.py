
# University Scholarship Allocation System

MIN_AGGREGATE = 75
MIN_SUBJECT_MARKS = 60
MIN_ATTENDANCE = 75
MAX_ANNUAL_INCOME = 250000

def evaluate_eligibility(student):
    reasons = []

    if student["aggregate"] < MIN_AGGREGATE:
        reasons.append("Aggregate marks below 75%")

    if any(mark < MIN_SUBJECT_MARKS
           for mark in student["subjects"].values()):
        reasons.append("One or more subjects below 60%")

    if student["attendance"] < MIN_ATTENDANCE:
        reasons.append("Attendance below 75%")

    if student["income"] > MAX_ANNUAL_INCOME:
        reasons.append("Family income exceeds Rs. 2,50,000")

    return reasons


def allocate_scholarships(students, scholarship_count):
    eligible = []
    rejected = []

    # Step 1: Check eligibility
    for student in students:
        reasons = evaluate_eligibility(student)

        if not reasons:
            eligible.append(student)
        else:
            rejected.append({
                "name": student["name"],
                "reasons": reasons
            })

    # Step 2: Rank eligible applicants
    # Priority:
    # 1. Higher aggregate marks
    # 2. Higher attendance
    # 3. Lower family income
    # 4. Alphabetical order of name
    eligible.sort(
        key=lambda s: (
            -s["aggregate"],
            -s["attendance"],
            s["income"],
            s["name"].casefold()
        )
    )

    # Step 3: Allocate scholarships
    selected = eligible[:max(0, scholarship_count)]
    waiting_list = eligible[max(0, scholarship_count):]

    return selected, waiting_list, rejected


def display_students(title, students):
    print(f"\n{'=' * 65}")
    print(title)
    print("=" * 65)

    if not students:
        print("No students found.")
        return

    for rank, student in enumerate(students, start=1):
        print(
            f"{rank}. {student['name']} | "
            f"Aggregate: {student['aggregate']}% | "
            f"Attendance: {student['attendance']}% | "
            f"Income: Rs. {student['income']:,}"
        )


# Sample applicant data
students = [
    {
        "name": "Ananya",
        "aggregate": 88,
        "subjects": {
            "Maths": 90,
            "Physics": 85,
            "Chemistry": 88
        },
        "attendance": 92,
        "income": 180000
    },
    {
        "name": "Bharath",
        "aggregate": 88,
        "subjects": {
            "Maths": 80,
            "Physics": 75,
            "Chemistry": 82
        },
        "attendance": 92,
        "income": 150000
    },
    {
        "name": "Charan",
        "aggregate": 72,
        "subjects": {
            "Maths": 70,
            "Physics": 65,
            "Chemistry": 75
        },
        "attendance": 90,
        "income": 100000
    },
    {
        "name": "Divya",
        "aggregate": 81,
        "subjects": {
            "Maths": 85,
            "Physics": 78,
            "Chemistry": 80
        },
        "attendance": 80,
        "income": 220000
    },
    {
        "name": "Esha",
        "aggregate": 79,
        "subjects": {
            "Maths": 75,
            "Physics": 58,
            "Chemistry": 84
        },
        "attendance": 95,
        "income": 100000
    }
]

# Main program
try:
    scholarship_count = int(
        input("Enter number of scholarships available: ")
    )

    if scholarship_count < 0:
        raise ValueError("Scholarship count cannot be negative.")

    selected, waiting_list, rejected = allocate_scholarships(
        students, scholarship_count
    )

    display_students("SCHOLARSHIP RECIPIENTS", selected)
    display_students("WAITING LIST", waiting_list)

    print(f"\n{'=' * 65}")
    print("INELIGIBLE APPLICANTS")
    print("=" * 65)

    if not rejected:
        print("No ineligible applicants.")
    else:
        for student in rejected:
            print(f"\n{student['name']}:")
            for reason in student["reasons"]:
                print(f"  - {reason}")

except ValueError as error:
    print("Invalid input:", error)

