import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar">
      <span className="brand">BalanceBoss AI</span>
      <Link to="/">Dashboard</Link>
      <Link to="/upload">Upload</Link>
      <Link to="/chat">Chat</Link>
    </nav>
  );
}
