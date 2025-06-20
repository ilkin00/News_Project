import './globals.css';
import Navbar from './components/Navbar';

export const metadata = {
  title: 'İlkin Haber',
  description: 'Güncel haberler sitesi',
};

export default function RootLayout({ children }) {
  return (
    <html lang="tr">
      <body>
        <Navbar />
        {children}
      </body>
    </html>
  );
}
