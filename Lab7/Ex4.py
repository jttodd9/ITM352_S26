def evaluate_purchases(recent_purchases, budget):
    results = []
    for expense in recent_purchases:
        if expense > budget:
            results.append("This purchase is over budget!")
        else:
            results.append("This purchase is within budget")
    return results


def run_tests():
    test_cases = [
        {
            "name": "sample list",
            "purchases": [36.13, 23.87, 183.35, 22.93, 11.62],
            "budget": 50.00,
            "expected": [
                "This purchase is within budget",
                "This purchase is within budget",
                "This purchase is over budget!",
                "This purchase is within budget",
                "This purchase is within budget",
            ],
        },
        {
            "name": "all over",
            "purchases": [51, 60],
            "budget": 50,
            "expected": [
                "This purchase is over budget!",
                "This purchase is over budget!",
            ],
        },
        {
            "name": "empty list",
            "purchases": [],
            "budget": 50,
            "expected": [],
        },
    ]

    for case in test_cases:
        actual = evaluate_purchases(case["purchases"], case["budget"])
        passed = actual == case["expected"]
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {case['name']}")
        if not passed:
            print("  expected:", case["expected"])
            print("  actual:  ", actual)


if __name__ == "__main__":
    run_tests()