
# Railway Fare and Reservation Calculator

# Sample fare rates per kilometer (in Rs.)
FARE_RATES = {
    "Sleeper": 1.50,
    "AC3": 2.50,
    "AC2": 3.50,
    "AC1": 5.00
}

# Distance-based base fare multipliers
DISTANCE_SLABS = [
    (100, 1.00),
    (300, 1.05),
    (500, 1.10),
    (float("inf"), 1.15)
]

RESERVATION_FEES = {
    "Sleeper": 20,
    "AC3": 40,
    "AC2": 50,
    "AC1": 60
}

# Illustrative age-based concession rates
CONCESSIONS = {
    "child": 0.50,       # Ages 5-11
    "senior": 0.40       # Ages 60 and above
}


def get_distance_multiplier(distance):
    for limit, multiplier in DISTANCE_SLABS:
        if distance <= limit:
            return multiplier
    return 1.0


def get_concession(age):
    if 5 <= age <= 11:
        return CONCESSIONS["child"]
    elif age >= 60:
        return CONCESSIONS["senior"]
    return 0.0


def calculate_fare(distance, travel_class, age):
    if distance <= 0:
        raise ValueError("Distance must be greater than zero.")

    if age < 0:
        raise ValueError("Age cannot be negative.")

    if travel_class not in FARE_RATES:
        raise ValueError("Invalid travel class.")

    # Calculate distance-based fare
    rate = FARE_RATES[travel_class]
    multiplier = get_distance_multiplier(distance)
    base_fare = distance * rate * multiplier

    # Apply age-based concession
    concession_rate = get_concession(age)
    concession_amount = base_fare * concession_rate
    discounted_fare = base_fare - concession_amount

    # Add reservation fee
    reservation_fee = RESERVATION_FEES[travel_class]
    total_fare = discounted_fare + reservation_fee

    return {
        "base_fare": round(base_fare, 2),
        "concession_rate": concession_rate,
        "concession_amount": round(concession_amount, 2),
        "reservation_fee": reservation_fee,
        "total_fare": round(total_fare, 2)
    }


def calculate_cancellation_penalty(total_fare, hours_before_departure):
    # Illustrative cancellation rules
    if hours_before_departure >= 48:
        penalty_rate = 0.10
    elif hours_before_departure >= 12:
        penalty_rate = 0.25
    elif hours_before_departure >= 4:
        penalty_rate = 0.50
    else:
        penalty_rate = 1.00

    penalty = total_fare * penalty_rate
    refund = total_fare - penalty

    return round(penalty, 2), round(refund, 2)


def main():
    passengers = []

    try:
        distance = float(input("Enter journey distance (km): "))

        if distance <= 0:
            raise ValueError("Distance must be positive.")

        number_of_passengers = int(
            input("Enter number of passengers: ")
        )

        if number_of_passengers <= 0:
            raise ValueError("Passenger count must be positive.")

        for i in range(number_of_passengers):
            print(f"\nPassenger {i + 1}")

            name = input("Enter passenger name: ").strip()
            if not name:
                raise ValueError("Passenger name cannot be empty.")

            age = int(input("Enter age: "))

            print("Available classes:", ", ".join(FARE_RATES))
            travel_class = input(
                "Choose travel class: "
            ).strip()

            # Normalize class input
            class_lookup = {
                name.lower(): name for name in FARE_RATES
            }
            travel_class = class_lookup.get(
                travel_class.lower()
            )

            if travel_class is None:
                raise ValueError("Invalid travel class.")

            fare_details = calculate_fare(
                distance, travel_class, age
            )

            passengers.append({
                "name": name,
                "age": age,
                "travel_class": travel_class,
                **fare_details
            })

        # Display fare details
        print("\n" + "=" * 75)
        print("RAILWAY FARE SUMMARY")
        print("=" * 75)

        grand_total = 0

        for passenger in passengers:
            print(f"\nPassenger: {passenger['name']}")
            print(f"Age: {passenger['age']}")
            print(f"Class: {passenger['travel_class']}")
            print(f"Base Fare: Rs. {passenger['base_fare']:.2f}")
            print(
                f"Concession: "
                f"{passenger['concession_rate'] * 100:.0f}%"
            )
            print(
                f"Concession Amount: "
                f"Rs. {passenger['concession_amount']:.2f}"
            )
            print(
                f"Reservation Fee: "
                f"Rs. {passenger['reservation_fee']:.2f}"
            )
            print(
                f"Total Fare: Rs. "
                f"{passenger['total_fare']:.2f}"
            )

            grand_total += passenger["total_fare"]

        print("\n" + "=" * 75)
        print(f"TOTAL BOOKING FARE: Rs. {grand_total:.2f}")
        print("=" * 75)

        # Optional cancellation calculation
        cancel = input(
            "\nCalculate cancellation refund? (yes/no): "
        ).strip().lower()

        if cancel == "yes":
            hours = float(input(
                "Hours remaining before departure: "
            ))

            if hours < 0:
                raise ValueError("Hours cannot be negative.")

            total_penalty = 0
            total_refund = 0

            print("\nCANCELLATION SUMMARY")

            for passenger in passengers:
                penalty, refund = calculate_cancellation_penalty(
                    passenger["total_fare"], hours
                )

                total_penalty += penalty
                total_refund += refund

                print(
                    f"{passenger['name']}: "
                    f"Penalty Rs. {penalty:.2f}, "
                    f"Refund Rs. {refund:.2f}"
                )

            print(f"Total Penalty: Rs. {total_penalty:.2f}")
            print(f"Total Refund: Rs. {total_refund:.2f}")

    except ValueError as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
