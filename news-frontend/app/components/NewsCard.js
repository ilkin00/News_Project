import Link from 'next/link';

export default function NewsCard({ news }) {
  return (
    <div className="border border-gray-300 rounded-lg p-4 shadow hover:shadow-lg transition cursor-pointer bg-white">
      <h2 className="text-xl font-semibold mb-2 text-gray-800">{news.title}</h2>
      <p className="text-gray-600 line-clamp-3">{news.content}</p>
      <Link 
        href={`/news/${news.slug}`} 
        className="inline-block mt-4 text-blue-600 hover:text-blue-800 underline font-medium"
      >
        Detaylar
      </Link>
    </div>
  );
}
