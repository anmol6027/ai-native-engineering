// =============================================================
// Topic 02 — JavaScript & TypeScript
// Build Task 02.2 — Where Does It Break?
//
// FILE 2 of 2: safe.ts  (TypeScript, with type checking)
//
// SAME function. SAME four calls. One difference:
// we declare what the types are supposed to be.
//
// DO NOT RUN THIS FILE. Compile it instead:
//
//   tsc safe.ts --noEmit --strict
//
// --noEmit  = check the code, don't produce output files
// --strict  = turn on maximum type checking
//
// The whole point is that it never gets to run.
// =============================================================


// The SAME function as unsafe.js — with three additions.
//
//   amount: number   the first argument must be a number
//   rate: number     the second argument must be a number
//   : number         the function must return a number
//
// That's it. Three declarations. That's the entire difference.
function calculateFee(amount: number, rate: number): number {
  return amount * rate
}


// -------------------------------------------------------------
// CASE 1 — Correct input.
// This one is fine. It compiles.
// -------------------------------------------------------------
const case1 = calculateFee(1500, 0.02)


// -------------------------------------------------------------
// CASE 2 — Amount as a string.
//
// In unsafe.js this returned 30 and looked correct.
// Here the compiler stops it.
// -------------------------------------------------------------
const case2 = calculateFee("1500", 0.02)


// -------------------------------------------------------------
// CASE 3 — Amount is null.
//
// In unsafe.js this returned 0 — a customer charged no fee,
// and the system reporting success.
// -------------------------------------------------------------
const case3 = calculateFee(null, 0.02)


// -------------------------------------------------------------
// CASE 4 — Amount missing entirely.
//
// In unsafe.js this returned NaN — still typed as "number".
// -------------------------------------------------------------
const case4 = calculateFee(0.02)


// -------------------------------------------------------------
// WHAT TO RECORD
//
// Run the compile command and count the errors.
// Note WHICH cases failed and what each message says.
//
// Then compare the two files:
//
//   unsafe.js  — ran to completion, returned wrong numbers,
//                nothing flagged anything
//
//   safe.ts    — never compiled, never ran, never shipped
//
// Same logic. Same bad inputs. The only question is WHEN
// you find out.
// -------------------------------------------------------------