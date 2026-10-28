
# Campus Event Financial Planning System

import math


def calculate_event_budget(
    venue_cost,
    equipment_cost,
    catering_per_person,
    transport_per_person,
    certificate_per_person,
    expected_participants,
    sponsorship,
    registration_fee
):
    # Step 1: Calculate fixed and variable costs
    fixed_cost = venue_cost + equipment_cost

    variable_cost_per_person = (
        catering_per_person
        + transport_per_person
        + certificate_per_person
    )

    variable_cost = variable_cost_per_person * expected_participants

    # Step 2: Calculate total event cost
    total_cost = fixed_cost + variable_cost

    # Step 3: Calculate sponsorship shortfall
    funding_shortfall = max(0, total_cost - sponsorship)

    # Step 4: Calculate required participant contribution
    participant_contribution = funding_shortfall / expected_participants

    # Step 5: Calculate registration income
    registration_income = registration_fee * expected_participants

    # Step 6: Calculate total available funds and surplus/deficit
    total_funds = sponsorship + registration_income
    surplus_or_deficit = total_funds - total_cost

    # Step 7: Calculate minimum registrations to break even
    # Each registration contributes the fee minus per-person costs.
    contribution_per_registration = (
        registration_fee - variable_cost_per_person
    )

    if contribution_per_registration > 0:
        break_even_registrations = max(
            0,
            math.ceil(
                (fixed_cost - sponsorship)
                / contribution_per_registration
            )
        )
    elif fixed_cost <= sponsorship:
        break_even_registrations = 0
    else:
        break_even_registrations = None

    return {
        "fixed_cost": fixed_cost,
        "variable_cost_per_person": variable_cost_per_person,
        "variable_cost": variable_cost,
        "total_cost": total_cost,
        "sponsorship": sponsorship,
        "funding_shortfall": funding_shortfall,
        "participant_contribution": participant_contribution,
        "registration_income": registration_income,
        "total_funds": total_funds,
        "surplus_or_deficit": surplus_or_deficit,
        "break_even_registrations": break_even_registrations
    }


def display_report(report, participants, registration_fee):
    print("\n" + "=" * 55)
    print("CAMPUS EVENT FINANCIAL REPORT")
    print("=" * 55)

    print("\nEXPENSE BREAKDOWN")
    print("-" * 55)
    print(f"Venue Cost:                 Rs. {venue_cost:.2f}")
    print(f"Equipment Cost:              Rs. {equipment_cost:.2f}")
    print(f"Variable Cost per Person:    Rs. {report['variable_cost_per_person']:.2f}")
    print(f"Total Variable Costs:        Rs. {report['variable_cost']:.2f}")
    print(f"Total Event Cost:            Rs. {report['total_cost']:.2f}")

    print("\nFUNDING DETAILS")
    print("-" * 55)
    print(f"Sponsorship:                 Rs. {report['sponsorship']:.2f}")
    print(f"Registration Fee:            Rs. {registration_fee:.2f}")
    print(f"Expected Participants:       {participants}")
    print(f"Registration Income:         Rs. {report['registration_income']:.2f}")
    print(f"Total Available Funds:       Rs. {report['total_funds']:.2f}")
    print(f"Sponsorship Funding Gap:     Rs. {report['funding_shortfall']:.2f}")
    print(f"Contribution per Participant: Rs. {report['participant_contribution']:.2f}")

    print("\nBREAK-EVEN ANALYSIS")
    print("-" * 55)

    if report["break_even_registrations"] is None:
        print("Break-even is not possible at this registration fee.")
        print("Increase the fee, reduce costs, or obtain more funding.")
    else:
        print(
            "Minimum registrations to break even:",
            report["break_even_registrations"]
        )

    print(f"Surplus / Deficit:            Rs. {report['surplus_or_deficit']:.2f}")

    if report["surplus_or_deficit"] > 0:
        print("Status: Event generates a surplus.")
    elif report["surplus_or_deficit"] < 0:
        print("Status: Event has a funding deficit.")
    else:
        print("Status: Event breaks even exactly.")


# Main program
if __name__ == "__main__":
    try:
        print("Enter event budget details (amounts in Rs.)")

        venue_cost = float(input("Venue cost: "))
        equipment_cost = float(input("Equipment cost: "))
        catering_per_person = float(input("Catering cost per person: "))
        transport_per_person = float(input("Transport cost per person: "))
        certificate_per_person = float(input("Certificate cost per person: "))

        expected_participants = int(
            input("Expected number of participants: ")
        )
        sponsorship = float(input("Total sponsorship received: "))
        registration_fee = float(input("Registration fee per participant: "))

        amounts = [
            venue_cost,
            equipment_cost,
            catering_per_person,
            transport_per_person,
            certificate_per_person,
            sponsorship,
            registration_fee
        ]

        if any(amount < 0 for amount in amounts):
            raise ValueError("Costs, sponsorship, and fee cannot be negative.")

        if expected_participants <= 0:
            raise ValueError("Expected participants must be greater than zero.")

        report = calculate_event_budget(
            venue_cost,
            equipment_cost,
            catering_per_person,
            transport_per_person,
            certificate_per_person,
            expected_participants,
            sponsorship,
            registration_fee
        )

        display_report(report, expected_participants, registration_fee)

    except ValueError as error:
        print("Invalid input:", error)
