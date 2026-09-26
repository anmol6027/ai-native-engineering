// This is a SERVER Component. No "use client" at the top.
// The fetch below runs on the server, before the browser
// receives anything.


type Post = { id: number; title: string };

async function getPosts(): Promise<Post[]> {
  const res = await fetch(
    "https://jsonplaceholder.typicode.com/posts?_limit=5",
    { next: { revalidate: 60 } }   // cache for 60 seconds
  );
  if (!res.ok) throw new Error("Failed to fetch posts");
  return res.json();
}

export default async function HomePage() {
  console.log("KITCHEN sees:", process.env.MY_SECRET);
  const posts = await getPosts();

  // This line prints in your TERMINAL, not the browser console.
  // That is the proof it ran on the server.
  console.log("Fetched on the server at", new Date().toISOString());

  return (
    <main className="mx-auto max-w-2xl p-8">
      <h1 className="mb-6 text-3xl font-bold">Posts</h1>
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