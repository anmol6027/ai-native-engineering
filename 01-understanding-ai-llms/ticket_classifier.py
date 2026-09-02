# =============================================================
# Topic 01 — Understanding AI & LLMs
# Build Task 01.2 — Ticket Classifier: Cost vs Consistency
#
# THE QUESTION THIS ANSWERS:
# A company gets 10,000 support emails a day. Can AI route them
# to the right team automatically? And what does it cost?
#
# WHAT WE PROVE:
#   1. The cheap approach gives DIFFERENT answers to the SAME email
#   2. The reliable approach costs measurably more
#   3. You can calculate the exact rupee difference
#
# HOW TO USE THIS FILE:
# Each block marked "CELL N" goes into its own Colab cell.
# Run them top to bottom.
# =============================================================
# =============================================================
# CELL 1 — INSTALL
# =============================================================
# Groq gives us free access to run large language models.
# The -q flag means "quiet" so we don't get pages of install logs.

get_ipython().system('pip install groq -q')
# =============================================================
# CELL 2 — SETUP
# =============================================================
# Connect to Groq using the API key stored in Colab's secrets.
#
# TO SET IT UP: click the key icon in Colab's left sidebar,
# add a secret named GROQ_API_KEY, and turn on "Notebook access".

from groq import Groq
from google.colab import userdata

client = Groq(api_key=userdata.get('GROQ_API_KEY'))

# The specific AI model we're using. Different models have
# different capabilities and different prices.
MODEL = "openai/gpt-oss-120b"

print("Connected. Model:", MODEL)
# =============================================================
# CELL 3 — THE PROBLEM
# =============================================================
# LABELS = the teams a ticket could be routed to.
# This is a Python list — an ordered collection of items.

LABELS = ["order_issue", "refund_request", "app_bug", "payment_issue", "account"]

# TICKET = one real customer complaint, stored as a string.
# The triple quotes let us write across multiple lines.
#
# WHY THIS TICKET IS DELIBERATELY MESSY:
# It contains THREE problems at once — an app crash, a double
# charge, and a refund request. A clean email like "my app is
# broken" is easy and proves nothing. Real customer emails are
# messy, and messy is where AI becomes unreliable.
# We are testing the hard case on purpose.

TICKET = """
Hi, I've been trying to place an order since yesterday.
The app froze twice during payment. Both times my bank sent
an SMS that money was deducted, but I never got an order
confirmation email. Now I can see two charges on my card
but nothing in my order history. I've been shopping with
you for 3 years and this has never happened. I just want
my money back. Also the app is still crashing when I open
the checkout page.
"""

print("Possible teams:", LABELS)
print("\nThe ticket:")
print(TICKET)
# =============================================================
# CELL 4 — APPROACH 1: ZERO-SHOT
# =============================================================
# "SHOT" MEANS "EXAMPLE". Zero-shot = zero examples given.
#
# We just tell the AI what the categories are and ask it to pick.
# No training, no examples, no guidance. The cheapest possible
# approach — and the one most teams try first.

def classify_zero_shot(ticket, temperature=0.2):
    """
    Classify a ticket with NO examples provided.

    temperature controls randomness:
      0.2 = predictable, sticks to the most likely answer
      0.8 = variable, more willing to pick less likely answers
    """

    # f-string lets us insert variables into text using {curly braces}
    # ', '.join(LABELS) turns the list into: "order_issue, refund_request, ..."
    prompt = f"""Classify this customer support ticket into exactly ONE intent.

Available intents: {', '.join(LABELS)}

Ticket: {ticket}

Reply with only the intent label. Nothing else."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,

        # max_tokens caps how much the model can write back.
        # We set this to 300, not 20. Here's why that matters:
        # this model THINKS internally before answering. If we cap
        # it too low, it runs out of room during its own reasoning
        # and returns an EMPTY answer — while still charging us.
        max_tokens=300,

        # reasoning_effort="low" tells it not to overthink.
        # Without this, it writes ~60 words of internal reasoning
        # to produce a one-word answer. You pay for all of it.
        reasoning_effort="low"
    )

    # We return three things:
    #   label = the actual answer
    #   input_tokens = how much text we SENT (cheap)
    #   output_tokens = how much text came BACK (5x more expensive)
    return {
        "label": response.choices[0].message.content.strip(),
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens
    }


result_zero = classify_zero_shot(TICKET)

print("ZERO-SHOT (no examples given)")
print("-" * 45)
print("Label        :", result_zero["label"])
print("Input tokens :", result_zero["input_tokens"])
print("Output tokens:", result_zero["output_tokens"])
print()
print("NOTE: the answer is ~3 tokens. The rest of the output")
print("tokens were the model reasoning internally. You paid for those.")
# =============================================================
# CELL 5 — APPROACH 2: FEW-SHOT
# =============================================================
# Few-shot = we show it a FEW EXAMPLES before asking.
#
# Same idea as training a new support agent: instead of saying
# "figure it out", you show them four examples of how it's done.
#
# THE HIDDEN COST: these examples get sent with EVERY SINGLE
# REQUEST. Forever. 10,000 tickets a day = 10,000 copies of
# these examples, every day.

EXAMPLES = """
Ticket: "My parcel says delivered but I never received it."
Intent: order_issue

Ticket: "You charged me twice for the same order. Please return one."
Intent: refund_request

Ticket: "The app closes every time I tap on my cart."
Intent: app_bug

Ticket: "My card was declined but money still got deducted."
Intent: payment_issue
"""


def classify_few_shot(ticket, temperature=0.2):
    """
    Same task as zero-shot, but with 4 examples included
    in the prompt to guide the model.
    """

    prompt = f"""Classify this customer support ticket into exactly ONE intent.

Available intents: {', '.join(LABELS)}

Here are examples of correct classifications:
{EXAMPLES}

Now classify this ticket.

Ticket: {ticket}

Reply with only the intent label. Nothing else."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=300,
        reasoning_effort="low"
    )

    return {
        "label": response.choices[0].message.content.strip(),
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens
    }


result_few = classify_few_shot(TICKET)

print("FEW-SHOT (4 examples given)")
print("-" * 45)
print("Label        :", result_few["label"])
print("Input tokens :", result_few["input_tokens"])
print("Output tokens:", result_few["output_tokens"])
print()

extra = result_few["input_tokens"] - result_zero["input_tokens"]
print(f"Those 4 examples cost an extra {extra} input tokens.")
print("Per request. Every request. Forever.")
# =============================================================
# CELL 6 — THE CONSISTENCY TEST  ** MOST IMPORTANT CELL **
# =============================================================
# THE PROBLEM THIS EXPOSES:
#
# An LLM is a PROBABILITY machine, not a rule engine.
# Ask it the same question twice, you can get different answers.
#
# Most teams test their AI once, see a correct answer, and ship it.
# They tested ACCURACY. They never tested CONSISTENCY.
# Those are different things — and consistency is what kills
# systems in production.
#
# WHY TEMPERATURE 0.8:
# We deliberately raise the randomness to EXPOSE the instability.
# At 0.2 it may look stable. Real production traffic is messier
# than one test, so we stress it on purpose.
#
# THE BUSINESS TRANSLATION:
# If this ticket routes to refunds on Monday and tech on Tuesday,
# customers get inconsistent treatment and nobody knows why.

print("Running the SAME ticket through zero-shot 5 times")
print("at temperature 1.5...\n")

answers = []

# range(5) gives us 0,1,2,3,4 — so this loop runs 5 times
for i in range(5):
    r = classify_zero_shot(TICKET, temperature=1.5)
    answers.append(r["label"])          # add this answer to our list
    print(f"  Run {i+1}: {r['label']}")

# set() removes duplicates. If all 5 answers were the same,
# the set has 1 item. If they differed, it has more.
unique_answers = set(answers)

print()
print("-" * 45)
print(f"Distinct answers: {len(unique_answers)}")
print(f"Answers seen    : {unique_answers}")
print()

if len(unique_answers) > 1:
    print(">>> Same ticket. Same model. Different answers.")
    print(">>> This is what breaks in production.")
else:
    print(">>> Consistent this run. Run the cell again —")
    print(">>> or raise temperature to 1.0 to expose the drift.")
# =============================================================
# CELL 7 — WHAT IT ACTUALLY COSTS
# =============================================================
# Few-shot is more reliable. But reliability has a price.
# This cell turns "more tokens" into a rupee figure a CTO
# can actually make a decision on.

# Pricing per MILLION tokens, in US dollars.
# Output costs more than input because input is processed all at
# once in parallel, while output is generated one token at a time.
#How the money is calculated

#Groq charges per million tokens:

#Input: $0.59 per million
#Output: $0.79 per million

#One zero-shot call:

#Input: 211 ÷ 1,000,000 × $0.59 = $0.000124
#Output: 46 ÷ 1,000,000 × $0.79 = $0.000036

#Total: $0.00016 per ticket. Fractions of a cent. Feels free.

INPUT_RATE_USD = 0.59
OUTPUT_RATE_USD = 0.79
USD_TO_INR = 88

# Business assumptions
CALLS_PER_DAY = 10_000     # the underscore is just for readability
DAYS_PER_MONTH = 30


def cost_per_call(input_tokens, output_tokens):
    """Cost in USD for a single API call."""
    input_cost = (input_tokens / 1_000_000) * INPUT_RATE_USD
    output_cost = (output_tokens / 1_000_000) * OUTPUT_RATE_USD
    return input_cost + output_cost


zero_call = cost_per_call(result_zero["input_tokens"], result_zero["output_tokens"])
few_call = cost_per_call(result_few["input_tokens"], result_few["output_tokens"])

zero_month_inr = zero_call * CALLS_PER_DAY * DAYS_PER_MONTH * USD_TO_INR
few_month_inr = few_call * CALLS_PER_DAY * DAYS_PER_MONTH * USD_TO_INR

print("TOKEN USAGE")
print("-" * 45)
print(f"Zero-shot : {result_zero['input_tokens']:>5} in  | {result_zero['output_tokens']:>4} out")
print(f"Few-shot  : {result_few['input_tokens']:>5} in  | {result_few['output_tokens']:>4} out")
print()

print(f"MONTHLY COST AT {CALLS_PER_DAY:,} TICKETS/DAY")
print("-" * 45)
print(f"Zero-shot : Rs {zero_month_inr:>10,.0f}")
print(f"Few-shot  : Rs {few_month_inr:>10,.0f}")
print(f"Difference: Rs {(few_month_inr - zero_month_inr):>10,.0f}")
print()
print("THE DECISION:")
print("Cheap option is unreliable. Reliable option costs more.")
print("Now you have the number to decide with.")
