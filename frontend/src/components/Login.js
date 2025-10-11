import React, { useEffect, useState } from "react";

export default function Login() {
  const [user, setUser] = useState(() => localStorage.getItem("mvp_user") || "");
  const [name, setName] = useState("");

  useEffect(() => {
    setName(user);
  }, [user]);

  function handleLogin(e) {
    e.preventDefault();
    if (!name || name.trim().length === 0) return alert("Please enter a name");
    localStorage.setItem("mvp_user", name.trim());
    setUser(name.trim());
    alert("Logged in as " + name.trim());
  }

  function handleLogout() {
    localStorage.removeItem("mvp_user");
    setUser("");
    setName("");
  }

  if (user) {
    return (
      <div style={{ marginBottom: 16 }}>
        Logged in as <strong>{user}</strong>
        <button onClick={handleLogout} style={{ marginLeft: 8 }}>
          Logout
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleLogin} style={{ marginBottom: 16 }}>
      <input
        placeholder="Your name (demo)"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button type="submit" style={{ marginLeft: 8 }}>
        Login
      </button>
    </form>
  );
}
