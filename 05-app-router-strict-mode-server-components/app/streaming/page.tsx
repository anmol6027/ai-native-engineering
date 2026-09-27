import { Suspense } from "react";
import FcpTimer from "@/app/fcp-timer";
import { getWelcome, getSales, getAiSummary } from "@/lib/data";

export const dynamic = "force-dynamic";

async function Welcome() {
  const welcome = await getWelcome();
  return <h1>{welcome}</h1>;
}

async function Sales() {
  const sales = await getSales();
  return <p>Sales: {sales}</p>;
}

async function AiSummary() {
  const summary = await getAiSummary();
  return <p>AI summary: {summary}</p>;
}

export default function StreamingPage() {
  return (
    <main style={{ padding: 40 }}>
    <FcpTimer />
      <Suspense fallback={<h1>Loading welcome...</h1>}>
        <Welcome />
      </Suspense>
      <Suspense fallback={<p>Loading sales...</p>}>
        <Sales />
      </Suspense>
      <Suspense fallback={<p>Generating AI summary...</p>}>
        <AiSummary />
      </Suspense>
    </main>
  );
}