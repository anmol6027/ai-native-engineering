# 07 — WCAG 2.1 AA: Can a Page Score 100 and Still Be Unusable?

## The question
Automated accessibility scanners (axe-core, and Lighthouse which runs axe-core rules) are said to catch about 57% of WCAG issues. What does the other part look like in practice, and does a perfect score mean a page is usable?

## Setup
- A small "QuickLoan" loan enquiry page, served locally with `python3.13 -m http.server 8080`
- Lighthouse 13.4.1 in Chrome DevTools, Accessibility only, Desktop
- Three versions of the same page:
  - `index.html` — 10 planted accessibility problems
  - `scanner-only.html` — only the problems Lighthouse reported are fixed; the rest left broken
  - `fixed.html` — all 10 problems fixed
- Each problem and fix is marked with a comment in the source

## The 10 planted problems

| # | Problem | Caught by Lighthouse? |
|---|---|---|
| 1 | `<html>` has no `lang` attribute | Yes |
| 2 | Logo image has no alt text | Yes |
| 3 | Low-contrast "Terms apply" text (about 1.7:1) | Yes |
| 4 | Placeholder text used instead of labels | No |
| 5 | Icon-only search button with no accessible name | Yes |
| 6 | Alt text is a filename ("img_4521.jpg") | No |
| 7 | "Submit" is a clickable div, not a button | No |
| 8 | Focus outline switched off (`outline: none`) | No |
| 9 | Popup closes only by mouse; Esc does nothing | No |
| 10 | Required fields indicated only by red colour | No |

Lighthouse caught 4 of 10. Prediction made before scanning: 7 of 10 classified correctly (wrong on #1, #7, #10).

## Measured results

| Version | Problems left | Lighthouse score | Close popup by keyboard | Submit by keyboard |
|---|---|---|---|---|
| index.html (broken) | 10 | 60 | No | No |
| scanner-only.html | 6 | 100 | No | No |
| fixed.html | 0 | 100 | Yes | Yes |

## Interpretation
- A page can score 100/100 and still block a keyboard user from completing its only task. scanner-only.html and fixed.html score the same; only one of them works.
- The scanner checks whether things exist and are formatted correctly: a language attribute, alt text, a button name, a contrast ratio. It cannot judge meaning (is the alt text useful? does red mean required?) or behaviour (can the popup be closed? can the form be submitted by keyboard?).
- The most damaging problem on the page, a Submit control a keyboard user cannot reach, was invisible to the scanner. A div with a click handler is not recognised as a control, so there is nothing for the scanner to check.
- Lighthouse states this itself: its "Additional items to manually check" list (keyboard focus, tab order, focus traps, focus on new content) is unscored and does not affect the 100.

## Side findings
- Placeholder-only fields passed the scanner, because a placeholder gives the field an accessible name. Accessibility practice still treats this as a failure: the hint disappears once the user starts typing.
- In the broken version, keyboard focus could Tab behind the open popup into the form under the overlay. The fixed version keeps focus inside the popup until it is closed.
- In text fields the blinking caret hid the missing focus outline; the missing outline was only obvious on the icon button.
- Testing pitfall: after running Lighthouse, keyboard input stays in the DevTools panel. Close DevTools before keyboard testing, or Esc and Tab will appear not to work.
- The fixed form marks name and mobile as `required`; pressing Submit with them empty shows the browser's "Please fill in this field" message. That is correct behaviour, not a failure.

## Limitations
- The 10 problems were chosen and planted for this test, so "4 of 10" is not a real-world detection rate. The finding is which kinds of problems a scanner can and cannot see.
- One Lighthouse run per version.
- No screen reader test was done; checks were keyboard-only.

## Run it

    python3.13 -m http.server 8080

Then open `http://localhost:8080/`, `http://localhost:8080/scanner-only.html` and `http://localhost:8080/fixed.html`. Run Lighthouse (Accessibility) on each, then close DevTools and try to close the popup and submit the form using only the keyboard.
