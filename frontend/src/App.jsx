import { useRoute } from './router';
import Home from './pages/Home';
import Auth from './pages/Auth';
import BookingPage from './pages/BookingPage';
import Dashboard from './pages/Dashboard';

export default function App() {
  const { path, navigate } = useRoute();

  // Intercept normal <a> clicks for internal links so it feels like an SPA
  function handleClick(e) {
    const anchor = e.target.closest('a');
    if (anchor && anchor.href.startsWith(window.location.origin) && !anchor.target) {
      e.preventDefault();
      navigate(new URL(anchor.href).pathname);
    }
  }

  let page;
  if (path === '/') {
    page = <Home navigate={navigate} />;
  } else if (path === '/login') {
    page = <Auth navigate={navigate} />;
  } else if (path === '/dashboard') {
    page = <Dashboard navigate={navigate} />;
  } else if (path.startsWith('/book/')) {
    const slug = path.replace('/book/', '');
    page = <BookingPage slug={slug} />;
  } else {
    page = (
      <div style={{ padding: 60, textAlign: 'center', color: 'var(--muted)' }}>
        Page not found.
      </div>
    );
  }

  return <div onClick={handleClick}>{page}</div>;
}
