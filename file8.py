
# Progressive Water Tariff Analysis

# Water consumption rates in rupees per 1000 liters (1 KL)
SLABS = [
    (10, 5),       # First 10 KL: Rs. 5 per KL
    (20, 10),      # Next 10 KL: Rs. 10 per KL
    (30, 20),      # Next 10 KL: Rs. 20 per KL
    (float("inf"), 30)  # Above 30 KL: Rs. 30 per KL
]

FIXED_FEE = 50
LATE_PAYMENT_PENALTY = 100
EXCESS_USAGE_LIMIT = 30


# Sample household data
# consumption is measured in kiloliters (KL)
households = {
    "Household A": {
        "consumption": 8,
        "previous_consumption": 10,
        "late_payment": False
    },
    "Household B": {
        "consumption": 18,
        "previous_consumption": 15,
        "late_payment": True
    },
    "Household C": {
        "consumption": 35,
        "previous_consumption": 28,
        "late_payment": False
    },
    "Household D": {
        "consumption": 45,
        "previous_consumption": 32,
        "late_payment": True
    }
}


def calculate_water_charge(consumption):
    """Calculate progressive water charges using consumption slabs."""

    if consumption < 0:
        raise ValueError("Consumption cannot be negative.")

    remaining = consumption
    previous_limit = 0
    water_charge = 0

    for upper_limit, rate in SLABS:
        slab_capacity = upper_limit - previous_limit
        slab_usage = min(remaining, slab_capacity)

        if slab_usage > 0:
            water_charge += slab_usage * rate
            remaining -= slab_usage

        previous_limit = upper_limit

        if remaining <= 0:
            break

    return water_charge


def calculate_bill(consumption, late_payment):
    """Calculate total water bill including fixed fee and penalty."""

    water_charge = calculate_water_charge(consumption)
    fixed_fee = FIXED_FEE

    penalty = (
        LATE_PAYMENT_PENALTY if late_payment else 0
    )

    total_bill = water_charge + fixed_fee + penalty

    return {
        "water_charge": water_charge,
        "fixed_fee": fixed_fee,
        "penalty": penalty,
        "total_bill": total_bill
    }


def analyze_household(name, data):
    """Analyze a household's water consumption."""

    consumption = data["consumption"]
    previous = data["previous_consumption"]
    late_payment = data["late_payment"]

    # Validate household data
    if consumption < 0 or previous < 0:
        raise ValueError(
            f"Invalid consumption data for {name}."
        )

    bill = calculate_bill(consumption, late_payment)

    change = consumption - previous

    if previous > 0:
        percentage_change = (change / previous) * 100
    elif consumption > 0:
        percentage_change = None
    else:
        percentage_change = 0

    if consumption > EXCESS_USAGE_LIMIT:
        usage_status = "Excessive Usage"
    elif consumption >= 20:
        usage_status = "High Usage"
    else:
        usage_status = "Normal Usage"

    return {
        "name": name,
        "consumption": consumption,
        "previous": previous,
        "change": change,
        "percentage_change": percentage_change,
        "usage_status": usage_status,
        **bill
    }


def main():
    print("=" * 95)
    print("             PROGRESSIVE WATER TARIFF ANALYSIS")
    print("=" * 95)

    results = []

    for name, data in households.items():
        results.append(analyze_household(name, data))

    # Display household comparison
    print(
        f"{'Household':<15}"
        f"{'Usage KL':>10}"
        f"{'Change KL':>12}"
        f"{'Water Fee':>12}"
        f"{'Fixed Fee':>12}"
        f"{'Penalty':>10}"
        f"{'Total Bill':>13}"
    )
    print("-" * 95)

    for result in results:
        print(
            f"{result['name']:<15}"
            f"{result['consumption']:>10.1f}"
            f"{result['change']:>+12.1f}"
            f"{result['water_charge']:>12.2f}"
            f"{result['fixed_fee']:>12.2f}"
            f"{result['penalty']:>10.2f}"
            f"{result['total_bill']:>13.2f}"
        )

    print("\n" + "=" * 55)
    print("             USAGE ANALYSIS")
    print("=" * 55)

    for result in results:
        print(f"\n{result['name']}")
        print(f"Current usage: {result['consumption']} KL")
        print(f"Previous usage: {result['previous']} KL")

        if result["percentage_change"] is None:
            print("Usage change: New consumption")
        else:
            print(
                f"Usage change: "
                f"{result['percentage_change']:+.2f}%"
            )

        print(f"Status: {result['usage_status']}")

        if result["change"] > 0:
            print("Trend: Consumption increased")
        elif result["change"] < 0:
            print("Trend: Consumption decreased")
        else:
            print("Trend: Consumption unchanged")

    # Identify the highest consumer
    highest = max(
        results,
        key=lambda item: item["consumption"]
    )

    print("\n" + "=" * 55)
    print("             SUMMARY")
    print("=" * 55)

    print(f"Total households: {len(results)}")
    print(
        f"Total water consumed: "
        f"{sum(r['consumption'] for r in results):.1f} KL"
    )
    print(
        f"Total revenue: Rs. "
        f"{sum(r['total_bill'] for r in results):.2f}"
    )
    print(
        f"Highest consumption: {highest['name']} "
        f"({highest['consumption']} KL)"
    )

    excessive = [
        r["name"] for r in results
        if r["usage_status"] == "Excessive Usage"
    ]

    print(
        "Excessive usage households:",
        ", ".join(excessive) if excessive else "None"
    )


if __name__ == "__main__":
    main()
