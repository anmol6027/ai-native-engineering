"use client";

import { useEffect, useState } from "react";

export default function FcpTimer() {
  const [fcp, setFcp] = useState<number | null>(null);

  useEffect(() => {
    const observer = new PerformanceObserver((list) => {
      const entry = list.getEntriesByName("first-contentful-paint")[0];
      if (entry) {
        const ms = Math.round(entry.startTime);
        setFcp(ms);
        console.log("FCP:", ms, "ms");
      }
    });
    observer.observe({ type: "paint", buffered: true });
    return () => observer.disconnect();
  }, []);

  return <p style={{ color: "gray" }}>FCP: {fcp ?? "measuring..."} ms</p>;
}