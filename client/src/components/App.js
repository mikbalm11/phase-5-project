import React, { useState, useEffect, createContext, useContext } from "react";
import LoginForm from "./LoginForm";
import SignUpForm from "./SignUpForm";
import NavBar from "./NavBar";
import UserOliveOils from "./UserOliveOils";
import UserOlives from "./UserOlives";
import UserProducers from "./UserProducers";

export const UserContext = createContext();

function App() {
  const [user, setUser] = useState(null);
  const [form, setForm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tabOpen, setTabOpen] = useState("oils");
  const [producers, setProducers] = useState([]);
  const [userProducers, setUserProducers] = useState([]);
  const [olives, setOlives] = useState([]);
  const [userOlives, setUserOlives] = useState([]);

  useEffect(() => {
    async function fetchInitialData() {
      try {
        const res = await fetch("/check_session", {
          credentials: "include",
        });
        if (!res.ok) throw new Error("Not logged in");
        const data = await res.json();
        setUser(data);
        setUserProducers(data.producers);
        setUserOlives(data.olives);

        const producerRes = await fetch("/producers");
        setProducers(await producerRes.json());

        const oliveRes = await fetch("/olives");
        setOlives(await oliveRes.json());

      } catch {
        setUser(null);
        setProducers([]);
        setUserProducers([]);
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

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {loading ? (
        <p>Loading...</p>
      ) : user ? (
        <div>
          <NavBar onLogout={handleLogout} onNavigate={setForm} />

            <div>
                <button onClick={() => setTabOpen("oils")}>Oils</button>
                <button onClick={() => setTabOpen("olives")}>Olives</button>
                <button onClick={() => setTabOpen("producers")}>Producers</button>
            </div>

            {tabOpen === "oils" && <UserOliveOils 
            producers={producers} 
            olives={olives}
            setProducers={setProducers} 
            setOlives={setOlives}
            userProducers={userProducers} 
            userOlives={userOlives}
            setUserProducers={setUserProducers}
            setUserOlives={setUserOlives}
             />}
            {tabOpen === "olives" && <UserOlives />}
            {tabOpen === "producers" && <UserProducers />}
        </div>
      ) : (
        
        <div>
          <NavBar onLogout={handleLogout} onNavigate={setForm} />
          {form === "login" && <LoginForm onLogin={handleLogin} />}
          {form === "signup" && <SignUpForm onLogin={handleLogin} />}
          {(form === "login" || form === "signup") && (
            <button onClick={() => setForm(null)}>Back</button>
          )}
          <div>Welcome to OliveCore 🫒</div>
        </div>
      )}
    </UserContext.Provider>
  );
}

export default App;
