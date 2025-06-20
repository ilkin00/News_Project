import Navbar from "./components/Navbar";
import NewsCard from "./components/NewsCard";

export default async function HomePage() {
  const res = await fetch("https://admin.ilkin.site/api/news/", { cache: "no-store" });
  if (!res.ok) {
    return <p>Haberler yüklenemedi.</p>;
  }
  const news = await res.json();

  return (
    <main className="p-6">
      <h1 className="text-3xl font-bold mb-4">Son Xəbərlər</h1>
      <div className="grid gap-4">
        {news.map(item => (
          <NewsCard key={item.id} news={item} />
        ))}
      </div>
    </main>
  );
}
