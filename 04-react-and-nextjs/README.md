# 04 — React & Next.js: Where Does Your API Key Actually Go?

## The question
In a Next.js app, which secrets can the browser see — and what decides it?

## Setup
- Next.js 16.3.4 (App Router, Turbopack), dev mode
- `app/page.tsx` — server component, fetches 5 posts on the server
- `app/client-version/page.tsx` — client component (`"use client"`), fetches the same posts in the browser
- `.env.local` with two fake keys (see `.env.example`):
  - `MY_SECRET=sk-fake-kitchen-111`
  - `NEXT_PUBLIC_MY_SECRET=sk-fake-table-222`
- Each page logs the env vars with `console.log`

## Measured results

| Where the code ran | Variable | Value seen |
|---|---|---|
| Server component (terminal) | `MY_SECRET` | `sk-fake-kitchen-111` |
| Client component (browser console) | `MY_SECRET` | `undefined` |
| Client component (browser console) | `NEXT_PUBLIC_MY_SECRET` | `sk-fake-table-222` |
| Client component (terminal, server pre-render) | both | real values for both |

## Interpretation
- Next.js blocks normal env vars from reaching the browser by default.
- The `NEXT_PUBLIC_` prefix is an explicit instruction to ship the value to every visitor. One prefix = public key.
- `"use client"` does not mean "browser only". Client components also run once on the server to pre-render, where they can read every env var. What the browser receives is what matters.

## Side findings
- `"use client"` must be the first line of the file. Placing a `console.log` above it produced 3 compile errors, including `useState`/`useEffect` being rejected as server-only violations.
- Opening the dev server via the network IP (`192.168.1.33:3000`) instead of `localhost` caused Next.js to block dev resources. The client page stayed stuck on "Loading..." because its JavaScript never hydrated. The server page rendered fine — it doesn't depend on browser JS.
- Browser logs appeared more than once per load (likely React Strict Mode double-invoking in dev, plus re-renders on state change). Not a bug.

## Limitations
- Tested in dev mode only; not yet verified against `npm run build && npm start`.
- Did not test passing a server secret to a client component as a prop — a known leak path not covered here.

## Run it

    cp .env.example .env.local
    npm install
    npm run dev

Open `http://localhost:3000` (check terminal) and `http://localhost:3000/client-version` (check browser console).
