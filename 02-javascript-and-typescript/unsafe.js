// =============================================================
// Topic 02 — JavaScript & TypeScript
// Build Task 02.2 — Where Does It Break?
//
// FILE 1 of 2: unsafe.js  (plain JavaScript, no type checking)
//
// THE SCENARIO:
// A payments company calculates transaction fees. The function
// takes an amount and a rate, returns the fee.
//
// WHAT WE'RE TESTING:
// What happens when the WRONG KIND of data gets passed in?
// Does the code stop? Or does it quietly return something wrong?
//
// RUN IT WITH:  node unsafe.js
// =============================================================


// The function. Notice: nothing here says what "amount" or
// "rate" are supposed to be. JavaScript doesn't ask.
function calculateFee(amount, rate) {
  return amount * rate
}


console.log("JAVASCRIPT — NO TYPE CHECKING")
console.log("=".repeat(50))
console.log()


// -------------------------------------------------------------
// CASE 1 — Correct input. A number and a number.
// This is what the developer intended.
// -------------------------------------------------------------
const case1 = calculateFee(1500, 0.02)
console.log("Case 1: calculateFee(1500, 0.02)")
console.log("  Result:", case1)
console.log("  Type  :", typeof case1)
console.log()


// -------------------------------------------------------------
// CASE 2 — Amount arrives as a STRING instead of a number.
//
// This happens constantly in real systems. Data from a form,
// a JSON API, or a database column can arrive as text.
// Watch carefully — this one is the dangerous case.
// -------------------------------------------------------------
const case2 = calculateFee("1500", 0.02)
console.log('Case 2: calculateFee("1500", 0.02)   <-- string')
console.log("  Result:", case2)
console.log("  Type  :", typeof case2)
console.log()


// -------------------------------------------------------------
// CASE 3 — Amount is null.
//
// A database field was empty. An API returned nothing.
// -------------------------------------------------------------
const case3 = calculateFee(null, 0.02)
console.log("Case 3: calculateFee(null, 0.02)")
console.log("  Result:", case3)
console.log("  Type  :", typeof case3)
console.log()


// -------------------------------------------------------------
// CASE 4 — Amount is missing entirely.
//
// Someone called the function with only one argument.
// -------------------------------------------------------------
const case4 = calculateFee(undefined, 0.02)
console.log("Case 4: calculateFee(undefined, 0.02)")
console.log("  Result:", case4)
console.log("  Type  :", typeof case4)
console.log()


// -------------------------------------------------------------
// BONUS — Same wrong input, different operator.
//
// This is the part worth understanding. A string and a number
// behave COMPLETELY differently depending on the operator.
// -------------------------------------------------------------
console.log("BONUS — same string input, two operators")
console.log("=".repeat(50))
console.log('  "1500" * 100  =', "1500" * 100, "  <-- multiplied")
console.log('  "1500" + 100  =', "1500" + 100, "  <-- joined as text")
console.log()


// -------------------------------------------------------------
// THE POINT
// -------------------------------------------------------------
console.log("=".repeat(50))
console.log("Every case above RAN. None of them stopped the program.")
console.log("Some returned NaN. One returned a number that looks correct.")
console.log("In production, this failure reaches a customer before")
console.log("it reaches a developer.")