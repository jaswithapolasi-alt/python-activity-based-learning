
# ATM Transaction Sequence Simulation

INITIAL_BALANCE = 5000.00
MAX_WITHDRAWAL = 10000.00
MAX_DAILY_WITHDRAWAL = 20000.00


def process_transactions(transactions, initial_balance):
    balance = initial_balance
    total_deposits = 0.0
    total_withdrawals = 0.0
    daily_withdrawals = 0.0
    successful_transactions = 0
    failed_transactions = 0
    transaction_history = []

    for index, transaction in enumerate(transactions, start=1):
        transaction_type = transaction["type"].lower()
        amount = transaction["amount"]
        status = ""
        message = ""

        # Validate transaction amount
        if amount <= 0:
            status = "FAILED"
            message = "Amount must be greater than zero."

        elif transaction_type == "deposit":
            balance += amount
            total_deposits += amount
            successful_transactions += 1
            status = "SUCCESS"
            message = "Deposit completed successfully."

        elif transaction_type == "withdrawal":
            if amount > MAX_WITHDRAWAL:
                status = "FAILED"
                message = "Exceeds single withdrawal limit."

            elif daily_withdrawals + amount > MAX_DAILY_WITHDRAWAL:
                status = "FAILED"
                message = "Exceeds daily withdrawal limit."

            elif amount > balance:
                status = "FAILED"
                message = "Insufficient account balance."

            else:
                balance -= amount
                daily_withdrawals += amount
                total_withdrawals += amount
                successful_transactions += 1
                status = "SUCCESS"
                message = "Withdrawal completed successfully."

        else:
            status = "FAILED"
            message = "Invalid transaction type."

        if status == "FAILED":
            failed_transactions += 1

        transaction_history.append({
            "number": index,
            "type": transaction_type.title(),
            "amount": amount,
            "status": status,
            "message": message,
            "balance": balance
        })

    return {
        "initial_balance": initial_balance,
        "final_balance": balance,
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
        "successful": successful_transactions,
        "failed": failed_transactions,
        "history": transaction_history
    }


def display_summary(result):
    print("\n" + "=" * 75)
    print("ATM TRANSACTION HISTORY")
    print("=" * 75)

    for transaction in result["history"]:
        print(
            f"\nTransaction #{transaction['number']}"
            f"\nType: {transaction['type']}"
            f"\nAmount: Rs. {transaction['amount']:.2f}"
            f"\nStatus: {transaction['status']}"
            f"\nMessage: {transaction['message']}"
            f"\nBalance: Rs. {transaction['balance']:.2f}"
        )

    print("\n" + "=" * 75)
    print("FINAL TRANSACTION SUMMARY")
    print("=" * 75)
    print(f"Initial Balance:       Rs. {result['initial_balance']:.2f}")
    print(f"Total Deposits:        Rs. {result['total_deposits']:.2f}")
    print(f"Total Withdrawals:     Rs. {result['total_withdrawals']:.2f}")
    print(f"Final Balance:         Rs. {result['final_balance']:.2f}")
    print(f"Successful Transactions: {result['successful']}")
    print(f"Failed Transactions:     {result['failed']}")
    print("=" * 75)


def main():
    balance = INITIAL_BALANCE
    transactions = []

    print("ATM TRANSACTION SIMULATION")
    print(f"Initial Balance: Rs. {balance:.2f}")
    print(f"Maximum Single Withdrawal: Rs. {MAX_WITHDRAWAL:.2f}")
    print(f"Maximum Daily Withdrawal: Rs. {MAX_DAILY_WITHDRAWAL:.2f}")

    while True:
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. Finish and display summary")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "3":
            break

        if choice not in ("1", "2"):
            print("Invalid choice. Please select 1, 2, or 3.")
            continue

        try:
            amount = float(input("Enter transaction amount (Rs.): "))

            transaction_type = (
                "deposit" if choice == "1" else "withdrawal"
            )

            transactions.append({
                "type": transaction_type,
                "amount": amount
            })

        except ValueError:
            print("Invalid amount. Please enter a number.")

    result = process_transactions(transactions, balance)
    display_summary(result)


if __name__ == "__main__":
    main()
