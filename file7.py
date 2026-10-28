
# Student Performance Trend Analysis

PASS_MARK = 40
WEAK_SUBJECT_MARK = 40

# Student marks in multiple examinations
students = {
    "Rahul": {
        "Maths": [55, 65, 75],
        "Science": [45, 50, 60],
        "English": [70, 68, 65]
    },
    "Priya": {
        "Maths": [85, 90, 95],
        "Science": [80, 85, 90],
        "English": [75, 80, 88]
    },
    "Amit": {
        "Maths": [35, 38, 30],
        "Science": [45, 35, 38],
        "English": [50, 55, 60]
    }
}


def classify_student(average):
    """Classify students according to their average score."""
    if average >= 85:
        return "Excellent"
    elif average >= 70:
        return "Very Good"
    elif average >= 55:
        return "Good"
    elif average >= PASS_MARK:
        return "Average"
    else:
        return "Needs Improvement"


def analyze_student(name, subjects):
    """Analyze performance across multiple examinations."""

    all_marks = []

    print("\n" + "=" * 55)
    print("Student Name:", name)
    print("=" * 55)

    print(
        f"{'Subject':<12}{'Exam 1':>10}"
        f"{'Exam 2':>10}{'Exam 3':>10}"
        f"{'Change':>10}"
    )
    print("-" * 55)

    weak_subjects = []
    improving_subjects = []
    declining_subjects = []

    for subject, marks in subjects.items():

        # Validate marks
        if len(marks) < 2:
            print(f"Skipping {subject}: Need at least 2 exams.")
            continue

        if any(
            not isinstance(mark, (int, float))
            or isinstance(mark, bool)
            or not 0 <= mark <= 100
            for mark in marks
        ):
            raise ValueError(
                f"Invalid marks for {name} in {subject}."
            )

        first_score = marks[0]
        last_score = marks[-1]
        change = last_score - first_score

        all_marks.extend(marks)

        print(
            f"{subject:<12}"
            f"{first_score:>10.1f}"
            f"{marks[1]:>10.1f}"
            f"{last_score:>10.1f}"
            f"{change:>+10.1f}"
        )

        # Check consistently weak subjects
        if all(mark < WEAK_SUBJECT_MARK for mark in marks):
            weak_subjects.append(subject)

        # Compare first and last examinations
        if change > 0:
            improving_subjects.append(subject)
        elif change < 0:
            declining_subjects.append(subject)

    if not all_marks:
        print("No valid examination marks available.")
        return

    average = sum(all_marks) / len(all_marks)

    # Calculate overall trend between first and last exams
    first_exam_avg = sum(
        marks[0] for marks in subjects.values()
        if len(marks) >= 2
    ) / sum(
        1 for marks in subjects.values()
        if len(marks) >= 2
    )

    last_exam_avg = sum(
        marks[-1] for marks in subjects.values()
        if len(marks) >= 2
    ) / sum(
        1 for marks in subjects.values()
        if len(marks) >= 2
    )

    overall_change = last_exam_avg - first_exam_avg

    print("-" * 55)
    print(f"Overall Average Score : {average:.2f}%")
    print(f"First Exam Average    : {first_exam_avg:.2f}%")
    print(f"Latest Exam Average   : {last_exam_avg:.2f}%")
    print(f"Overall Score Change  : {overall_change:+.2f}")

    print(
        "Performance Category  :",
        classify_student(average)
    )

    if overall_change > 0:
        print("Overall Trend         : Improving")
    elif overall_change < 0:
        print("Overall Trend         : Declining")
    else:
        print("Overall Trend         : Stable")

    print("\nImproving Subjects:")
    print(", ".join(improving_subjects) or "None")

    print("\nDeclining Subjects:")
    print(", ".join(declining_subjects) or "None")

    print("\nConsistently Weak Subjects:")
    print(", ".join(weak_subjects) or "None")


def main():
    print("=" * 55)
    print("       STUDENT PERFORMANCE TREND ANALYSIS")
    print("=" * 55)

    for name, subjects in students.items():
        analyze_student(name, subjects)

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
