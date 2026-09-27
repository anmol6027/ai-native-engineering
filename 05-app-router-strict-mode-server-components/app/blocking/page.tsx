import { getWelcome, getSales, getAiSummary } from "@/lib/data";
import FcpTimer from "@/app/fcp-timer";

export const dynamic = "force-dynamic";

export default async function BlockingPage() {
  // Wait for ALL three before sending anything
  const [welcome, sales, summary] = await Promise.all([
    getWelcome(),
    getSales(),
    getAiSummary(),
  ]);

  return (
    <main style={{ padding: 40 }}>
        <FcpTimer />
      <h1>{welcome}</h1>
      <p>Sales: {sales}</p>
      <p>AI summary: {summary}</p>
    </main>
  );
}