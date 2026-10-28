
from datetime import datetime, timedelta
import math

# Parking rates per hour
VEHICLE_RATES = {
    "bike": 20,
    "car": 50,
    "truck": 100
}

# Maximum parking fee per 24-hour period
DAILY_LIMITS = {
    "bike": 150,
    "car": 400,
    "truck": 800
}

# Additional charges
OVERNIGHT_FEE = 50
LATE_EXIT_PENALTY = 100
LOST_TICKET_PENALTY = 200


def get_valid_datetime(prompt):
    """Read and validate date and time."""
    while True:
        value = input(prompt).strip()

        try:
            return datetime.strptime(
                value, "%Y-%m-%d %H:%M"
            )
        except ValueError:
            print(
                "Invalid input! Use YYYY-MM-DD HH:MM "
                "(Example: 2026-10-28 09:30)"
            )


def calculate_parking_fee(
    entry_time,
    exit_time,
    vehicle_type,
    late_exit=False,
    lost_ticket=False
):
    """Calculate the total parking fee."""

    if vehicle_type not in VEHICLE_RATES:
        raise ValueError("Invalid vehicle category.")

    if exit_time <= entry_time:
        raise ValueError(
            "Exit time must be later than entry time."
        )

    duration = exit_time - entry_time
    total_hours = duration.total_seconds() / 3600

    # Charge for every started hour
    billable_hours = math.ceil(total_hours)

    hourly_rate = VEHICLE_RATES[vehicle_type]
    daily_limit = DAILY_LIMITS[vehicle_type]

    # Calculate fee separately for each 24-hour period
    full_days = int(total_hours // 24)
    remaining_hours = total_hours % 24

    parking_fee = full_days * daily_limit
    parking_fee += min(
        math.ceil(remaining_hours) * hourly_rate,
        daily_limit
    )

    # Count overnight periods crossed
    overnight_periods = (
        exit_time.date() - entry_time.date()
    ).days

    overnight_fee = max(0, overnight_periods) * OVERNIGHT_FEE

    # Penalties
    penalty = 0

    if late_exit:
        penalty += LATE_EXIT_PENALTY

    if lost_ticket:
        penalty += LOST_TICKET_PENALTY

    total_fee = parking_fee + overnight_fee + penalty

    return {
        "duration_hours": round(total_hours, 2),
        "billable_hours": billable_hours,
        "parking_fee": parking_fee,
        "overnight_fee": overnight_fee,
        "penalty": penalty,
        "total_fee": total_fee
    }


def main():
    print("=" * 40)
    print("   SMART PARKING FEE MANAGEMENT")
    print("=" * 40)

    print("\nVehicle categories:")
    print("1. Bike  - Rs. 20/hour")
    print("2. Car   - Rs. 50/hour")
    print("3. Truck - Rs. 100/hour")

    vehicle_options = {
        "1": "bike",
        "2": "car",
        "3": "truck"
    }

    while True:
        choice = input(
            "\nSelect vehicle category (1/2/3): "
        ).strip()

        if choice in vehicle_options:
            vehicle_type = vehicle_options[choice]
            break

        print("Invalid choice! Please select 1, 2, or 3.")

    entry_time = get_valid_datetime(
        "Enter entry time (YYYY-MM-DD HH:MM): "
    )

    exit_time = get_valid_datetime(
        "Enter exit time (YYYY-MM-DD HH:MM): "
    )

    while exit_time <= entry_time:
        print(
            "Error: Exit time must be after entry time."
        )
        exit_time = get_valid_datetime(
            "Enter a valid exit time (YYYY-MM-DD HH:MM): "
        )

    late_exit_input = input(
        "Was the vehicle collected after the allowed "
        "exit deadline? (yes/no): "
    ).strip().lower()

    lost_ticket_input = input(
        "Was the parking ticket lost? (yes/no): "
    ).strip().lower()

    late_exit = late_exit_input in ("yes", "y")
    lost_ticket = lost_ticket_input in ("yes", "y")

    result = calculate_parking_fee(
        entry_time,
        exit_time,
        vehicle_type,
        late_exit,
        lost_ticket
    )

    print("\n" + "=" * 40)
    print("           PARKING RECEIPT")
    print("=" * 40)
    print(f"Vehicle type      : {vehicle_type.title()}")
    print(f"Entry time        : {entry_time}")
    print(f"Exit time         : {exit_time}")
    print(
        f"Parking duration  : "
        f"{result['duration_hours']} hours"
    )
    print(
        f"Billable hours    : "
        f"{result['billable_hours']}"
    )
    print(
        f"Parking fee       : Rs. "
        f"{result['parking_fee']:.2f}"
    )
    print(
        f"Overnight fee     : Rs. "
        f"{result['overnight_fee']:.2f}"
    )
    print(
        f"Penalty           : Rs. "
        f"{result['penalty']:.2f}"
    )
    print("-" * 40)
    print(
        f"TOTAL AMOUNT      : Rs. "
        f"{result['total_fee']:.2f}"
    )
    print("=" * 40)


if __name__ == "__main__":
    main()
