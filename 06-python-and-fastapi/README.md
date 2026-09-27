# 06 — Python & FastAPI: Does Type Checking Stop Bad Data?

## The question
FastAPI + Pydantic reject requests with the wrong data types. Is that enough to keep bad loan applications out of the system?

## Setup
- Python 3.13.15 in a virtual environment (`.venv`), packages pinned in `requirements.txt`
- FastAPI 0.141.1, Pydantic 2.13.5
- `main.py` — one loan intake API with three versions of the same endpoint:
  - `/v1/no-checks` — accepts any JSON
  - `/v2/types-only` — Pydantic model with types only (`str`, `int`), as built in class
  - `/v3/types-and-rules` — same types plus business rules via `Field`:
    - name: 2–100 characters
    - monthly income: greater than 0, max ₹1 crore
    - loan amount: greater than 0, max ₹5 crore
    - purpose: 3–200 characters
- `measure.py` — sends 10 applications to all three endpoints using FastAPI's `TestClient` and counts outcomes

## Test set (10 applications)
- 2 good: a normal application, a high-earner application
- 7 bad: income as text "abc", missing purpose, negative income, negative loan amount, loan amount 0, empty name, income ₹999 crore/month
- 1 grey: income sent as the text "85000" instead of a number

## Measured results

| Case | v1 no checks | v2 types only | v3 types + rules |
|---|---|---|---|
| Valid application | ACCEPT | ACCEPT | ACCEPT |
| Valid, high earner | ACCEPT | ACCEPT | ACCEPT |
| Income is text "abc" | ACCEPT | REJECT | REJECT |
| Missing purpose | ACCEPT | REJECT | REJECT |
| Negative income | ACCEPT | ACCEPT | REJECT |
| Negative loan amount | ACCEPT | ACCEPT | REJECT |
| Loan amount 0 | ACCEPT | ACCEPT | REJECT |
| Empty name | ACCEPT | ACCEPT | REJECT |
| Income ₹999 crore/month | ACCEPT | ACCEPT | REJECT |
| Income as text "85000" | ACCEPT | ACCEPT | ACCEPT |

| Endpoint | Bad accepted | Good rejected |
|---|---|---|
| v1 no checks | 7 / 7 | 0 / 2 |
| v2 types only | 5 / 7 | 0 / 2 |
| v3 types + rules | 0 / 7 | 0 / 2 |

## Interpretation
- Type checking stops malformed data (wrong type, missing field) but not nonsensical data. 5 of 7 bad applications passed the types-only version.
- Four business rules stopped all 7 bad applications without rejecting either good one.
- Type rules are a developer decision. Business rules (income above zero, loan ceilings) are policy and should be owned by the business, not guessed in code.
- The grey case: Pydantic's default "lax mode" silently converted the text "85000" into the number 85000 in both v2 and v3. The API does not reject sloppy input; it fixes it quietly. Pydantic's strict mode would reject it.
- When v3 rejects, the 422 response names the field, the rule and the input (e.g. `monthly_income`, "Input should be greater than 0", `-50000`) with no custom error code written.

## Side findings
- macOS ships with Python 3.9.6, which is end-of-life; installed 3.13 via Homebrew (`brew install python@3.13`), following the "newest minus one" rule.
- `uvicorn --reload` watched the `.venv` folder and reloaded on changes to installed packages (likely caused by cloud-folder sync). Fix: `--reload-exclude ".venv/*"`.
- "Attribute app not found in module main" meant the file was not saved yet.

## Limitations
- The bad cases and rule limits were chosen for this test; a real lender's policy would set different thresholds. The pattern is the finding, not the exact 5/7.
- Only request validation was tested — no database, no authentication.
- Strict mode was not tested.

## Run it

    python3.13 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python measure.py

To explore the API in a browser:

    uvicorn main:app --reload --reload-exclude ".venv/*"

Then open `http://localhost:8000/docs`.
