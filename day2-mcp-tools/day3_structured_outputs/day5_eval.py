import json


# 1. The core evaluation function that tests an agent's output
def evaluate_output(raw_output: str) -> bool:
    """Returns True if the output passes all checks, raises AssertionError otherwise."""
    # Check 1: Must be valid JSON
    try:
        parsed = json.loads(raw_output)
    except ValueError:
        raise AssertionError(
            "❌ Schema Failure: Output is distorted text, not valid JSON."
        )

    # Check 2: Vital keys must exist
    required_keys = ["amount", "category", "merchant"]
    for key in required_keys:
        if key not in parsed:
            raise AssertionError(f"❌ Structural Failure: Missing key '{key}'.")

    # Check 3: Data type integrity check
    if not (
        isinstance(parsed["amount"], float) or isinstance(parsed["amount"], int)
    ):
        raise AssertionError("❌ Type Failure: 'amount' field must be numeric.")

    return True


# 2. Test runner using a matrix of passing and failing scenarios
def run_production_test_matrices():
    print("🧪 Running Production Test Matrices...\n")

    test_cases = [
        {
            "name": "Case 1: Valid Perfect Payload",
            "data": '{"amount": 42.50, "category": "Meals", "merchant": "Starbucks"}',
            "should_pass": True,
        },
        {
            "name": "Case 2: Failure - Corrupted Text / Broken JSON",
            "data": '{"amount": 42.50, "category": "Meals", "merchant": "Starbucks"',  # Missing closing brace
            "should_pass": False,
        },
        {
            "name": "Case 3: Failure - Missing Critical Key (merchant)",
            "data": '{"amount": 15.00, "category": "Software"}',  # Missing merchant
            "should_pass": False,
        },
        {
            "name": "Case 4: Failure - Wrong Data Type (String instead of Float)",
            "data": '{"amount": "forty-two dollars", "category": "Meals", "merchant": "Subway"}',
            "should_pass": False,
        },
    ]

    passed_count = 0

    for case in test_cases:
        print(f"🔄 Testing -> {case['name']}")
        try:
            evaluate_output(case["data"])
            # If it passes and was supposed to pass, that's a win!
            if case["should_pass"]:
                print("✅ Passed as expected.")
                passed_count += 1
            else:
                print(
                    "❌ CRITICAL FAILURE: The suite wrongly marked a bad payload as VALID."
                )

        except AssertionError as error:
            # If it threw an assertion error and was supposed to fail, your evaluation suite worked!
            if not case["should_pass"]:
                print(f"✅ Defended Successfully! Guardrail caught it: {error}")
                passed_count += 1
            else:
                print(f"❌ CRITICAL FAILURE: Valid code was rejected: {error}")

        print("-" * 50)

    print(
        f"\n🎉 MATRIX RUN COMPLETE: Passed ({passed_count}/{len(test_cases)}) safety benchmarks."
    )


if __name__ == "__main__":
    run_production_test_matrices()

    