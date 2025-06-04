import React, { useState, useEffect } from "react";
import LoginForm from "./LoginForm";
import SignUpForm from "./SignUpForm";
import NavBar from "./NavBar";
import UserOlives from "./UserOlives";

function App() {
    const [user, setUser] = useState(null);
    const [form, setForm] = useState(null);
    const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchInitialData() {
      try {
        const res = await fetch("/check_session", {
          credentials: "include",
        });
        if (!res.ok) throw new Error("Not logged in");
        const data = await res.json();

        setUser(data);

      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    }
    fetchInitialData();
  }, []);

  async function handleLogin() {
    try {
      const sessionRes = await fetch("/check_session", {
        credentials: "include",
      });
      if (!sessionRes.ok) throw new Error("Login session check failed");

      const userData = await sessionRes.json();
      setUser(userData);

      setForm(null);
    } catch (err) {
      console.error("Login failed:", err);
    }
  }

  function handleLogout() {
    fetch("/logout", { method: "DELETE", credentials: "include" }).then((r) => {
      if (r.ok) {
        setUser(null);
        setForm(null);
      }
    });
  }

  if (loading) return <p>Loading...</p>;

  if (user) {
    return (
      <div className="app-logged-in">
        <NavBar user={user} onLogout={handleLogout} onNavigate={setForm} />
        <UserOlives user={user} />
      </div>
    );
  }

  return (
    <div className="app-container">
      <NavBar user={user} onLogout={handleLogout} onNavigate={setForm} />
      {form === "login" && <LoginForm onLogin={handleLogin} />}
      {form === "signup" && <SignUpForm onLogin={handleLogin} />}
      {(form === "login" || form === "signup") && (
        <button onClick={() => setForm(null)} className="btn btn-secondary">
          Back
        </button>
      )}
    </div>
  );
}

export default App;
