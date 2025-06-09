import { useContext } from "react";
import { UserContext } from "./App";

function NavBar({ onLogout, onNavigate }) {
  const { user } = useContext(UserContext);

  return (
    <nav>
      <h2>OliveCore 🫒</h2>

      {user ? (
        <div>
          <span>Welcome, {user.username}!</span>
          <button onClick={onLogout}>Logout</button>
        </div>
      ) : (
        <div>
          <button onClick={() => onNavigate("login")}>Login</button>
          <button onClick={() => onNavigate("signup")}>Sign Up</button>
        </div>
      )}
    </nav>
  );
}

export default NavBar;
