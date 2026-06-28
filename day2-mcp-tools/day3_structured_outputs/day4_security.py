import json


# Mocking a parsed expense payload from Day 3
def simulate_agent_flow(expense_data):
    print("\n--- 🛡️ Running Agent Input Guardrails ---")

    # 1. Input Guardrail Checklist
    if expense_data["amount"] <= 0:
        print("❌ GUARDRAIL TRIGGERED: Amount must be greater than zero.")
        return "Transaction Blocked"

    if not expense_data["merchant"].strip():
        print("❌ GUARDRAIL TRIGGERED: Missing merchant name.")
        return "Transaction Blocked"

    # 2. Human-in-the-Loop (HITL) Policy Triage Gate
    # Any transaction over $100 requires a manager's keystroke approval
    if expense_data["amount"] > 100.00:
        print(
            f"\n⚠️ WARNING: High-value transaction detected from '{expense_data['merchant']}'."
        )
        print(f"💰 Total Amount: ${expense_data['amount']:.2f}")

        # The system pauses completely and waits for keyboard input
        human_choice = input(
            "👉 Do you explicitly authorize this expense? (yes/no): "
        )

        if human_choice.strip().lower() != "yes":
            print("🛑 TRANSACTION TERMINATED: Refused by Human Orchestrator.")
            return "Rejected by Human"

        print("✅ Authorization verified by Human.")

    # 3. Execution Processing Core
    print(
        f"🚀 SUCCESS: Expense of ${expense_data['amount']} processed cleanly!"
    )
    return "Approved & Finalized"


# --- Run Evaluation Tests ---
if __name__ == "__main__":
    # Test 1: Low value (Should pass automatically)
    low_expense = {
        "amount": 42.50,
        "category": "Meals",
        "merchant": "Starbucks",
        "transaction_date": "2026-06-18",
    }
    simulate_agent_flow(low_expense)

    # Test 2: High value (Will pause the terminal and ask you to type 'yes' or 'no')
    high_expense = {
        "amount": 1250.00,
        "category": "Equipment",
        "merchant": "Apple Store",
        "transaction_date": "2026-06-20",
    }
    simulate_agent_flow(high_expense)