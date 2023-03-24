import { Link } from "react-router-dom";
import logo from "../logo.jpg";

function Navbar() {
  return (
    <header>
      <div className="logo">
        <img src={logo} alt="Train logo" />
        <h1>Train World</h1>
      </div>
      <nav>
        <Link to="/">Home</Link>
      </nav>
    </header>
  );
}

export default Navbar;
