
# Tuple-Based Employee Shift Conflict Detection

# Each shift is a tuple:
# (Employee ID, Employee Name, Start Time, End Time)

shifts = [
    (101, "Rahul", 9, 13),
    (102, "Priya", 10, 14),
    (101, "Rahul", 12, 16),
    (103, "Amit", 14, 18),
    (104, "Sneha", 9, 12),
    (102, "Priya", 15, 19),
    (105, "Kiran", 11, 15)
]


def validate_shifts(shifts):
    """Validate employee shift tuples."""

    for shift in shifts:
        if len(shift) != 4:
            raise ValueError("Each shift must contain 4 values.")

        employee_id, name, start, end = shift

        if not isinstance(employee_id, int):
            raise ValueError("Employee ID must be an integer.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Employee name cannot be empty.")

        if not isinstance(start, (int, float)) or isinstance(start, bool):
            raise ValueError("Start time must be numeric.")

        if not isinstance(end, (int, float)) or isinstance(end, bool):
            raise ValueError("End time must be numeric.")

        if start < 0 or end > 24 or start >= end:
            raise ValueError(
                f"Invalid shift time for employee {name}."
            )


def detect_conflicts(shifts):
    """Find overlapping shifts for the same employee."""

    conflicts = []
    conflicting_employees = []

    # Compare every pair of shifts
    for i in range(len(shifts)):
        for j in range(i + 1, len(shifts)):

            shift1 = shifts[i]
            shift2 = shifts[j]

            id1, name1, start1, end1 = shift1
            id2, name2, start2, end2 = shift2

            # Check whether shifts belong to the same employee
            if id1 == id2:

                # Two intervals overlap if each starts
                # before the other one ends.
                if start1 < end2 and start2 < end1:

                    conflicts.append((shift1, shift2))

                    if id1 not in conflicting_employees:
                        conflicting_employees.append(id1)

    return conflicts, conflicting_employees


def display_shifts(shifts):
    """Display all scheduled employee shifts."""

    print("\nEMPLOYEE SHIFT SCHEDULE")
    print("-" * 55)
    print(
        f"{'ID':<8}{'Name':<15}"
        f"{'Start':<12}{'End':<10}"
    )
    print("-" * 55)

    for employee_id, name, start, end in shifts:
        print(
            f"{employee_id:<8}{name:<15}"
            f"{start:02}:00{'':<6}{end:02}:00"
        )


def display_conflicts(conflicts, conflicting_employees):
    """Display conflicting shift assignments."""

    print("\nSHIFT CONFLICT REPORT")
    print("-" * 55)

    if not conflicts:
        print("No overlapping shifts found.")
        return

    for shift1, shift2 in conflicts:
        print(f"\nEmployee: {shift1[1]} (ID: {shift1[0]})")
        print(
            f"Shift 1: {shift1[2]:02}:00 - "
            f"{shift1[3]:02}:00"
        )
        print(
            f"Shift 2: {shift2[2]:02}:00 - "
            f"{shift2[3]:02}:00"
        )

        overlap_start = max(shift1[2], shift2[2])
        overlap_end = min(shift1[3], shift2[3])

        print(
            f"Conflict duration: "
            f"{overlap_end - overlap_start} hour(s)"
        )

    print("\nEMPLOYEES WITH CONFLICTING SCHEDULES")
    print("-" * 55)

    for employee_id in conflicting_employees:
        for shift in shifts:
            if shift[0] == employee_id:
                print(f"{shift[1]} (ID: {employee_id})")
                break


def main():
    print("=" * 55)
    print(" TUPLE-BASED EMPLOYEE SHIFT CONFLICT DETECTION")
    print("=" * 55)

    try:
        validate_shifts(shifts)

        display_shifts(shifts)

        conflicts, employees = detect_conflicts(shifts)

        display_conflicts(conflicts, employees)

    except ValueError as error:
        print("Input Error:", error)


if __name__ == "__main__":
    main()
