import React, { useState } from "react";

function SignUpForm({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setIsLoading(true);
    setErrors([]);

    fetch("/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, password }),
    }).then((r) => {
      setIsLoading(false);
      if (r.ok) {
        r.json().then((user) => onLogin(user));
      } else {
        r.json().then((err) => {
          if (err.errors) {
            setErrors(err.errors);
          } else {
            setErrors(["Signup failed"]);
          }
        });
      }
    });
  }

  return (
    <form onSubmit={handleSubmit} className="signup-form">
      <div className="form-group">
        <label>
          Username:{" "}
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="form-input"
          />
        </label>
      </div>
      <div className="form-group">
        <label>
          Password:{" "}
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="form-input"
          />
        </label>
      </div>
      <button type="submit" disabled={isLoading} className="form-button">
        {isLoading ? "Signing Up..." : "Sign Up"}
      </button>
      {errors.length > 0 && (
        <div className="form-errors">
          {errors.map((error, idx) => (
            <p key={idx}>{error}</p>
          ))}
        </div>
      )}
    </form>
  );
}

export default SignUpForm;
