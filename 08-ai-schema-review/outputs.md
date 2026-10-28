# Topic 08 — Prompts and raw outputs

## Starting schema (included in both prompts)

```prisma
model Borrower {
  id    String @id @default(cuid())
  name  String
  phone String @unique
  loans Loan[]
}

model Loan {
  id         String   @id @default(cuid())
  borrowerId String
  borrower   Borrower @relation(fields: [borrowerId], references: [id])
}
```

## Prompt A (vague)

> Add EMI tracking: each loan has an EMI payment record showing the date it was paid and the amount. Give me only the updated schema.

## Prompt B (checklist)

> Add EMI tracking: each loan has an EMI payment record showing the date it was paid and the amount. Give me only the updated schema.
>
> Before you answer, review your design against these 4 questions and fix anything that fails:
> 1. Could any relationship be one-to-many over time?
> 2. Which fields will be queried most, and do they have indexes?
> 3. Are all dates stored as real date/time types?
> 4. Are all money amounts stored as exact decimals, not floats?

---

## ChatGPT — Prompt A (3/4: no index)

```prisma
model Borrower {
  id    String @id @default(cuid())
  name  String
  phone String @unique
  loans Loan[]
}

model Loan {
  id         String        @id @default(cuid())
  borrowerId String
  borrower   Borrower      @relation(fields: [borrowerId], references: [id])
  emiPayments EmiPayment[]
}

model EmiPayment {
  id     String   @id @default(cuid())
  loanId String
  loan   Loan     @relation(fields: [loanId], references: [id])
  paidAt DateTime
  amount Decimal  @db.Decimal(12, 2)
}
```

## ChatGPT — Prompt B (4/4)

```prisma
model Borrower {
  id    String @id @default(cuid())
  name  String
  phone String @unique
  loans Loan[]
}

model Loan {
  id          String       @id @default(cuid())
  borrowerId  String
  borrower    Borrower     @relation(fields: [borrowerId], references: [id])
  emiPayments EmiPayment[]

  @@index([borrowerId])
}

model EmiPayment {
  id     String   @id @default(cuid())
  loanId String
  loan   Loan     @relation(fields: [loanId], references: [id])
  paidAt DateTime
  amount Decimal  @db.Decimal(12, 2)

  @@index([loanId, paidAt])
}
```

---

## Gemini — Prompt A (2/4: no index, amount as Float)

```prisma
model Borrower {
  id    String @id @default(cuid())
  name  String
  phone String @unique
  loans Loan[]
}

model Loan {
  id         String       @id @default(cuid())
  borrowerId String
  borrower   Borrower     @relation(fields: [borrowerId], references: [id])
  emis       EmiPayment[]
}

model EmiPayment {
  id       String   @id @default(cuid())
  loanId   String
  loan     Loan     @relation(fields: [loanId], references: [id])
  amount   Float
  paidDate DateTime
}
```

## Gemini — Prompt B (4/4)

```prisma
model Borrower {
  id    String @id @default(cuid())
  name  String
  phone String @unique
  loans Loan[]
}

model Loan {
  id         String       @id @default(cuid())
  borrowerId String
  borrower   Borrower     @relation(fields: [borrowerId], references: [id])
  emis       EmiPayment[]

  @@index([borrowerId])
}

model EmiPayment {
  id       String   @id @default(cuid())
  loanId   String
  loan     Loan     @relation(fields: [loanId], references: [id])
  amount   Decimal
  paidDate DateTime

  @@index([loanId])
}
```

---

## Claude — Prompt A (4/4), fresh incognito run (counted)

```prisma
model Borrower {
  id    String @id @default(cuid())
  name  String
  phone String @unique
  loans Loan[]
}

model Loan {
  id          String       @id @default(cuid())
  borrowerId  String
  borrower    Borrower     @relation(fields: [borrowerId], references: [id])
  emiPayments EmiPayment[] // one-to-many: a loan has many EMIs over its tenure, not one record
}

model EmiPayment {
  id     String   @id @default(cuid())
  loanId String
  loan   Loan     @relation(fields: [loanId], references: [id])
  paidOn DateTime
  amount Decimal  // Decimal, not Float: Float causes rounding errors with money

  @@index([loanId])
}
```

## Claude — Prompt B (4/4, redesigned into two tables) (counted)

```prisma
model Borrower {
  id    String @id @default(cuid())
  name  String
  phone String @unique
  loans Loan[]
}

model Loan {
  id           String           @id @default(cuid())
  borrowerId   String
  borrower     Borrower         @relation(fields: [borrowerId], references: [id])
  installments EmiInstallment[]

  @@index([borrowerId]) // Prisma does not auto-index foreign keys on Postgres
}

// Q1 fix: one EMI can be paid in several partial payments over time,
// so the schedule (what's due) is separate from payments (what was paid).
// This also lets you detect missed/overdue EMIs, which a payments-only table can't.
model EmiInstallment {
  id            String       @id @default(cuid())
  loanId        String
  loan          Loan         @relation(fields: [loanId], references: [id])
  installmentNo Int
  dueDate       DateTime     @db.Date           // Q3: calendar date, no time component
  amountDue     Decimal      @db.Decimal(12, 2) // Q4: exact decimal
  payments      EmiPayment[]

  @@unique([loanId, installmentNo])
  @@index([loanId, dueDate]) // Q2: "upcoming/overdue EMIs for this loan"
  @@index([dueDate])         // Q2: "all EMIs due today/this week" across loans
}

model EmiPayment {
  id            String         @id @default(cuid())
  installmentId String
  installment   EmiInstallment @relation(fields: [installmentId], references: [id])
  amount        Decimal        @db.Decimal(12, 2) // Q4: exact decimal
  paidAt        DateTime                          // Q3: full timestamp of payment

  @@index([installmentId, paidAt]) // Q2: payment history per installment
  @@index([paidAt])                // Q2: daily/monthly collection reports
}
```

---

## Discarded Claude Prompt A runs (not counted)

Run 1 explained itself against the exact checklist (comments such as "not one" and "not Float") despite the vague prompt. Run 2 was almost identical to the Prompt B output above, including the two-table redesign and the same comments. Both suggest the chat had access to earlier context. The fresh incognito run above replaced them.
