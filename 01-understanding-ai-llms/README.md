# 01 — Ticket Classifier: Cost vs Consistency

## The problem

A company routing 10,000 support emails a day wants AI to
classify each one to the right team. Two questions before
shipping: does it answer consistently, and what does it cost
at that volume?

## What I tested

Same support ticket, two approaches:

- **Zero-shot** — categories only, no examples
- **Few-shot** — same prompt plus four worked examples

Then ran the zero-shot version five times to check whether
the answer held. Raised temperature to 1.5 to try and break it.

The ticket was deliberately ambiguous — app crash, double
charge, and a refund request in one message.

## What I found

| | Zero-shot | Few-shot |
|---|---|---|
| Input tokens | 211 | 300 |
| Output tokens | 46 | 44 |
| Consistency | 5/5 @ temp 1.5 | not tested |
| Cost @ 10k/day | ₹4,246/mo | ₹5,590/mo |

Zero-shot held across all five runs. The four examples added
89 tokens per request — **₹16,000 a year at this volume** —
and returned the same label on the single run tested.

## What I'd ship

Zero-shot. Not because it's cheaper, but because I measured
it and the alternative added cost without adding reliability.

The wider point: classification is a constrained task. The
model picks from five options rather than generating freely,
so temperature has less room to shift the outcome. The
instability everyone warns about lives in the generative
parts of a pipeline, not here.

## Also learned

Setting `max_tokens=20` on a reasoning model returns an
**empty string** while still billing for the tokens. The
model spends its budget on internal reasoning and never
reaches the answer. Silent failure, real cost.

Fixed with `max_tokens=300` and `reasoning_effort="low"`.

## Run it

Google Colab. Needs a free Groq API key stored in Colab
secrets as `GROQ_API_KEY`.
