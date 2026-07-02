import './Home.css';

export default function Home({ navigate }) {
  return (
    <div className="home">
      <div className="home-mark">
        <span className="home-number">01</span>
        <span className="home-label">Now Serving</span>
      </div>
      <h1 className="home-title">Bookings that hold<br />their place in line.</h1>
      <p className="home-sub">
        A booking page for your salon or barbershop. Clients pick a time,
        you get a ticket, no more phone tag.
      </p>
      <div className="home-actions">
        <button className="btn-primary" onClick={() => navigate('/login')}>
          Business login
        </button>
        <button className="btn-ghost" onClick={() => navigate('/book/dgt-exclusives-hair-salon')}>
          View a sample booking page →
        </button>
      </div>
    </div>
  );
}
