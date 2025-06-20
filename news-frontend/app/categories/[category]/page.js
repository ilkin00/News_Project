export default function CategoryPage({ params }) {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Kateqoriya: {params.category}</h1>
      {/* Bu sayfada kategoriye özel haberleri gösterebilirsin */}
    </div>
  );
}
