import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="bg-gray-900 p-4 text-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto flex gap-6">
        <Link href="/">
          <a className="font-bold text-lg hover:text-blue-400 transition">Ana Sayfa</a>
        </Link>
        <Link href="/categories">
          <a className="hover:text-blue-400 transition">Kategoriler</a>
        </Link>
        <Link href="/news">
          <a className="hover:text-blue-400 transition">Haberler</a>
        </Link>
        <Link href="/about">
          <a className="hover:text-blue-400 transition">Hakkında</a>
        </Link>
      </div>
    </nav>
  );
}
