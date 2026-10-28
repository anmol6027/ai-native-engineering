# 08 — AI-Assisted Schema Design: Do Today's AIs Still Make the Classic Mistakes?

## The question
AI-written database schemas are known to fail in four ways: wrong cardinality, missing indexes, dates stored as text, and money stored as Float. Do current AI assistants still make these mistakes? And does a short, reusable review checklist in the prompt fix them?

## Setup
- Three AI assistants, free web versions, October 2026: ChatGPT, Gemini, Claude
- Each prompt run in a fresh chat with memory off (incognito / temporary chat)
- A new scenario (loan EMI payments) rather than the lecture's example, so the AI could not have memorised it
- Same starting Prisma schema (Borrower, Loan) in both prompts

### Prompt A — vague
Written the way a busy product manager would write it. The singular wording ("an EMI payment record") is the cardinality trap:

> Add EMI tracking: each loan has an EMI payment record showing the date it was paid and the amount. Give me only the updated schema.

### Prompt B — the same request plus a generic review
> Before you answer, review your design against these 4 questions and fix anything that fails:
> 1. Could any relationship be one-to-many over time?
> 2. Which fields will be queried most, and do they have indexes?
> 3. Are all dates stored as real date/time types?
> 4. Are all money amounts stored as exact decimals, not floats?

The checklist does not give away the answers. It can be reused for any table.

Full prompts and all outputs: `outputs.md`

## Scoring

| Check | Pass | Fail |
|---|---|---|
| Cardinality | Loan has a list of payments; `loanId` not `@unique` | One payment per loan |
| Index | `loanId` indexed (alone or as the first column of an index) | No index on `loanId` |
| Date | Payment date is `DateTime` | `String` |
| Money | Amount is `Decimal` | `Float` |

## Measured results

| Assistant | Prompt A (vague) | Prompt B (checklist) |
|---|---|---|
| ChatGPT | 3 / 4 — no index | 4 / 4 |
| Gemini | 2 / 4 — no index, amount as `Float` | 4 / 4 |
| Claude | 4 / 4 | 4 / 4 (redesigned into two tables) |
| **Total** | **9 / 12** | **12 / 12** |

| Classic mistake | Assistants that made it with Prompt A |
|---|---|
| Wrong cardinality | 0 of 3 |
| Dates as text | 0 of 3 |
| Missing index | 2 of 3 |
| Money as Float | 1 of 3 |

## Interpretation
- The obvious mistakes did not appear. All three assistants modelled one loan with many EMIs despite the singular wording, and all used real date types.
- The mistakes that survived are the invisible ones. A missing index causes no error, only slowness as data grows. Float money causes no error, only drift in totals. Neither is caught by "it compiled and migrated".
- A four-line generic checklist raised the score from 9/12 to 12/12.
- With the checklist, Claude redesigned the model into an installment schedule plus a payments table, to support partial payments and missed-EMI detection. Reasonable, but it is a design change nobody asked for. Scope changes need a human decision, not just a review.

## Side findings
- PostgreSQL does not automatically index foreign key columns such as `loanId`.
- ChatGPT's `@@index([loanId, paidAt])` is a two-column index. It serves both "this loan's EMIs" and "this loan's EMIs in a date range", like a phone book sorted by surname, then first name.
- Gemini's Prompt B used plain `Decimal` without a size. It is exact, so it passes, but a finance reviewer would add `@db.Decimal(12, 2)`.
- Claude's Prompt B used `@db.Date` for the due date (calendar date, no time), which suits a due date better than a timestamp.

## Test integrity
- The first two Claude Prompt A runs were discarded. One explained itself against the exact checklist despite the vague prompt; the second was almost identical to the Prompt B output. Both point to shared context. A third run in a fresh incognito chat is the one counted.
- A later Claude Prompt B paste was character-for-character identical to Prompt A, so it was treated as a copy mistake; the original Prompt B run is the one counted.
- This analysis was written with help from Claude, which is one of the assistants tested. That is a further reason not to read the results as a ranking.

## Limitations
- One run per assistant per prompt. This shows a pattern, not a ranking of tools.
- Model versions were not recorded; free web versions change often.
- Schemas were scored by reading them, not by running migrations or load tests.
