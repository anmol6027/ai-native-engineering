from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

base = {
    "applicant_name": "Priya Sharma",
    "monthly_income": 85000,
    "amount_requested": 500000,
    "purpose": "Home renovation",
}

cases = [
    ("Valid application", "good", base),
    ("Valid, high earner", "good", {**base, "monthly_income": 900000, "amount_requested": 20000000}),
    ("Income is text 'abc'", "bad", {**base, "monthly_income": "abc"}),
    ("Missing purpose", "bad", {k: v for k, v in base.items() if k != "purpose"}),
    ("Negative income", "bad", {**base, "monthly_income": -50000}),
    ("Negative loan amount", "bad", {**base, "amount_requested": -100000}),
    ("Loan amount 0", "bad", {**base, "amount_requested": 0}),
    ("Empty name", "bad", {**base, "applicant_name": ""}),
    ("Income 999 crore/month", "bad", {**base, "monthly_income": 9_990_000_000}),
    ("Income as text '85000'", "grey", {**base, "monthly_income": "85000"}),
]

versions = ["/v1/no-checks", "/v2/types-only", "/v3/types-and-rules"]
bad_accepted = {v: 0 for v in versions}
good_rejected = {v: 0 for v in versions}

print(f"{'Case':28} {'Kind':5} {'v1':>7} {'v2':>7} {'v3':>7}")
print("-" * 58)
for name, kind, payload in cases:
    row = []
    for v in versions:
        accepted = client.post(v, json=payload).status_code == 200
        row.append("ACCEPT" if accepted else "REJECT")
        if kind == "bad" and accepted:
            bad_accepted[v] += 1
        if kind == "good" and not accepted:
            good_rejected[v] += 1
    print(f"{name:28} {kind:5} {row[0]:>7} {row[1]:>7} {row[2]:>7}")

print()
for v in versions:
    print(f"{v:22}  bad accepted: {bad_accepted[v]}/7   good rejected: {good_rejected[v]}/2")