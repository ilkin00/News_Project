import React from 'react';

export default async function NewsDetail({ params }) {
  const res = await fetch(`https://admin.ilkin.site/api/news/${params.slug}/`, {
    cache: 'no-store', // Her defasında güncel veri çekmek için
  });
  
  if (!res.ok) {
    return <div className="p-6 text-red-600">Haber bulunamadı.</div>;
  }

  const data = await res.json();

  return (
    <div className="container mx-auto p-6 max-w-3xl">
      <h1 className="text-3xl font-bold mb-4 text-gray-900">{data.title}</h1>
      <article className="prose prose-lg text-gray-700" dangerouslySetInnerHTML={{ __html: data.content }} />
    </div>
  );
}
