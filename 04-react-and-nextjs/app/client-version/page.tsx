"use client";   // <-- this changes everything


import { useEffect, useState } from "react";

type Post = { id: number; title: string };

export default function ClientVersion() {
  console.log("TABLE sees normal:", process.env.MY_SECRET);
console.log("TABLE sees public:", process.env.NEXT_PUBLIC_MY_SECRET);
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // This runs in the BROWSER, after the page loads.
    console.log("Fetching from the browser at", new Date().toISOString());

    fetch("https://jsonplaceholder.typicode.com/posts?_limit=5")
      .then((res) => res.json())
      .then((data: Post[]) => {
        setPosts(data);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <main className="mx-auto max-w-2xl p-8">
        <h1 className="mb-6 text-3xl font-bold">Posts (client)</h1>
        <p>Loading...</p>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-2xl p-8">
      <h1 className="mb-6 text-3xl font-bold">Posts (client)</h1>
      <ul className="space-y-2">
        {posts.map((post) => (
          <li key={post.id} className="rounded border p-3">
            {post.title}
          </li>
        ))}
      </ul>
    </main>
  );
}