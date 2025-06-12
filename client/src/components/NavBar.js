import { useContext } from "react";
import { UserContext } from "./App";

function NavBar({ onLogout, onNavigate }) {
  const { user } = useContext(UserContext);

  return (
    <nav className="navbar">
      <h2 className="navbar-logo">OliveCore 🫒</h2>

      {user ? (
        <div className="navbar-user-section">
          <span className="navbar-welcome">Welcome, {user.username}!</span>
          <button className="navbar-button logout-button" onClick={onLogout}>Logout</button>
        </div>
      ) : (
        <div className="navbar-auth-buttons">
          <button className="navbar-button" onClick={() => onNavigate("login")}>Login</button>
          <button className="navbar-button" onClick={() => onNavigate("signup")}>Sign Up</button>
        </div>
      )}
    </nav>
  );
}

export default NavBar;
