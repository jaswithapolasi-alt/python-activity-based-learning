
# Multi-Plan Telecommunications Cost Optimization System

def evaluate_plan(plan, usage, required_validity, budget):
    # Check validity requirement
    if plan["validity"] < required_validity:
        return None

    # Calculate excess usage
    excess_data = max(0, usage - plan["data_limit"])

    # Calculate excess charges
    excess_charge = excess_data * plan["extra_charge_per_gb"]

    # Calculate total cost
    total_cost = plan["price"] + excess_charge

    # Check budget constraint
    eligible = total_cost <= budget

    return {
        "name": plan["name"],
        "base_price": plan["price"],
        "data_limit": plan["data_limit"],
        "usage": usage,
        "excess_data": excess_data,
        "excess_charge": excess_charge,
        "validity": plan["validity"],
        "total_cost": total_cost,
        "eligible": eligible
    }


def optimize_plans(plans, usage, required_validity, budget):
    results = []

    for plan in plans:
        result = evaluate_plan(
            plan, usage, required_validity, budget
        )

        if result is not None:
            results.append(result)

    # Sort by total cost, then by longer validity
    results.sort(
        key=lambda p: (
            p["total_cost"],
            -p["validity"],
            p["name"].casefold()
        )
    )

    eligible_plans = [
        plan for plan in results if plan["eligible"]
    ]

    return results, eligible_plans


def display_results(results):
    if not results:
        print("\nNo plans meet the required validity.")
        return

    print("\n" + "=" * 95)
    print("MOBILE PLAN COST COMPARISON")
    print("=" * 95)

    print(
        f"{'Plan':<15}"
        f"{'Base Price':>12}"
        f"{'Data (GB)':>12}"
        f"{'Excess (GB)':>13}"
        f"{'Extra Cost':>13}"
        f"{'Total Cost':>13}"
        f"{'Status':>12}"
    )
    print("-" * 95)

    for plan in results:
        status = "Eligible" if plan["eligible"] else "Over budget"

        print(
            f"{plan['name']:<15}"
            f"{plan['base_price']:>12.2f}"
            f"{plan['data_limit']:>12.1f}"
            f"{plan['excess_data']:>13.1f}"
            f"{plan['excess_charge']:>13.2f}"
            f"{plan['total_cost']:>13.2f}"
            f"{status:>12}"
        )


def main():
    # Sample mobile plans (illustrative prices in INR)
    plans = [
        {
            "name": "Basic",
            "price": 199,
            "data_limit": 10,
            "validity": 28,
            "extra_charge_per_gb": 20
        },
        {
            "name": "Standard",
            "price": 299,
            "data_limit": 25,
            "validity": 56,
            "extra_charge_per_gb": 15
        },
        {
            "name": "Premium",
            "price": 399,
            "data_limit": 50,
            "validity": 84,
            "extra_charge_per_gb": 10
        },
        {
            "name": "Unlimited",
            "price": 499,
            "data_limit": 100,
            "validity": 84,
            "extra_charge_per_gb": 5
        }
    ]

    try:
        usage = float(input("Enter expected data usage (GB): "))
        required_validity = int(
            input("Enter minimum required validity (days): ")
        )
        budget = float(input("Enter your budget (Rs.): "))

        if usage < 0 or required_validity <= 0 or budget < 0:
            raise ValueError(
                "Usage and budget must be non-negative; "
                "validity must be positive."
            )

        results, eligible_plans = optimize_plans(
            plans, usage, required_validity, budget
        )

        display_results(results)

        print("\n" + "=" * 50)
        print("OPTIMAL PLAN RECOMMENDATION")
        print("=" * 50)

        if eligible_plans:
            best = eligible_plans[0]

            print("Recommended Plan :", best["name"])
            print("Base Price       : Rs.", best["base_price"])
            print("Excess Data      :", best["excess_data"], "GB")
            print("Excess Charges   : Rs.", best["excess_charge"])
            print("Total Cost       : Rs.", best["total_cost"])
            print("Validity         :", best["validity"], "days")
            print("Remaining Budget : Rs.",
                  round(budget - best["total_cost"], 2))
        else:
            print("No plan satisfies all constraints.")
            print("Try increasing your budget or reducing")
            print("your required validity or data usage.")

    except ValueError as error:
        print("Invalid input:", error)


if __name__ == "__main__":
    main()
