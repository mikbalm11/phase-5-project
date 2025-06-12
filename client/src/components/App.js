import React, { useState, useEffect, createContext, useContext } from "react";
import LoginForm from "./LoginForm";
import SignUpForm from "./SignUpForm";
import NavBar from "./NavBar";
import UserOliveOils from "./UserOliveOils";
import UserOlives from "./UserOlives";
import UserProducers from "./UserProducers";

export const UserContext = createContext();

function App() {
  const [user, setUser] = useState({ oils: [] });
  const [form, setForm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tabOpen, setTabOpen] = useState("oils");
  const [producers, setProducers] = useState([]);
  const [userProducers, setUserProducers] = useState([]);
  const [olives, setOlives] = useState([]);
  const [userOlives, setUserOlives] = useState([]);
  const [extraData, setExtraData] = useState({});

  function applyUserData(data) {
    const userObj = data.user || { oils: [] };
    setUser(userObj);
    setUserProducers((data.userProducers || []));
    setUserOlives((data.userOlives || []));
    setExtraData(data.extraData || {});
  }

  useEffect(() => {
    async function fetchInitialData() {
      try {
        const res = await fetch("/check_session", {
          credentials: "include",
        });
        if (!res.ok) throw new Error("Not logged in");
        const data = await res.json();
        applyUserData(data);

        const producerRes = await fetch("/producers");
        setProducers(await producerRes.json());

        const oliveRes = await fetch("/olives");
        setOlives(await oliveRes.json());

        setForm(null);
      } catch {
        setUser(null);
        setProducers([]);
        setUserProducers([]);
        setOlives([]);
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

      const data = await sessionRes.json();
      applyUserData(data);

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

function handleAddOil(newOil) {
  setUser((prev) => ({
    ...prev,
    oils: [...prev.oils, newOil],
  }));

  if (newOil.olive) {
    setUserOlives((prev) => {
      const found = prev.find((o) => o.id === newOil.olive.id);
      if (found) {
        return prev.map((olive) =>
          olive.id === newOil.olive.id
            ? { ...olive, oils: [...olive.oils, newOil] }
            : olive
        );
      } else {
        return [...prev, { ...newOil.olive, oils: [newOil] }];
      }
    });
  }

  if (newOil.producer) {
    setUserProducers((prev) => {
      const found = prev.find((p) => p.id === newOil.producer.id);
      if (found) {
        return prev.map((producer) =>
          producer.id === newOil.producer.id
            ? { ...producer, oils: [...producer.oils, newOil] }
            : producer
        );
      } else {
        return [...prev, { ...newOil.producer, oils: [newOil] }];
      }
    });
  }
}

  function handleEditOil(updatedOil) {
    setUser((prev) => ({
      ...prev,
      oils: prev.oils.map((oil) => (oil.id === updatedOil.id ? updatedOil : oil)),
    }));

    setUserOlives((prevOlives) =>
      prevOlives.map((olive) => {
        if (!olive.oils.find((o) => o.id === updatedOil.id)) return olive;
        return {
          ...olive,
          oils: olive.oils.map((oil) =>
            oil.id === updatedOil.id ? updatedOil : oil
          ),
        };
      })
    );

    setUserProducers((prevProducers) =>
      prevProducers.map((producer) => {
        if (!producer.oils.find((o) => o.id === updatedOil.id)) return producer;
        return {
          ...producer,
          oils: producer.oils.map((oil) =>
            oil.id === updatedOil.id ? updatedOil : oil
          ),
        };
      })
    );
  }
    function handleDeleteOil(deletedId) {
    setUser((prev) => ({
      ...prev,
      oils: prev.oils.filter((oil) => oil.id !== deletedId),
    }));

    setUserOlives((prevOlives) =>
      prevOlives
        .map((olive) => {
          const filteredOils = olive.oils.filter((oil) => oil.id !== deletedId);
          if (filteredOils.length === 0) return null;
          return { ...olive, oils: filteredOils };
        })
        .filter(Boolean)
    );

    setUserProducers((prevProducers) =>
      prevProducers
        .map((producer) => {
          const filteredOils = producer.oils.filter((oil) => oil.id !== deletedId);
          if (filteredOils.length === 0) return null;
          return { ...producer, oils: filteredOils };
        })
        .filter(Boolean)
    );
  }

  return (
    <UserContext.Provider value={{ 
      user, setUser,
      producers, setProducers,
      olives, setOlives,
      userProducers, setUserProducers,
      userOlives, setUserOlives,
      extraData,
      handleAddOil, handleEditOil, handleDeleteOil,
      }}>
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

            {tabOpen === "oils" && <UserOliveOils />}
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
