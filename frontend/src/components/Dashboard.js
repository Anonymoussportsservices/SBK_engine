import React, { useEffect, useState } from "react";
import { fetchOdds, placeBet } from "../api";

export default function Dashboard() {
  const [odds, setOdds] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stake, setStake] = useState(1);
  const [placingId, setPlacingId] = useState(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchOdds();
      setOdds(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error(e);
      setError("Failed to load odds. Check API URL / CORS.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    const id = setInterval(load, 30000); // refresh every 30 seconds
    return () => clearInterval(id);
  }, []);

  async function handleBet(o) {
    if (!window.confirm(`Place ${stake} unit(s) on ${o.selection} @ ${o.price}?`)) return;

    const payload = {
      user_id: localStorage.getItem("mvp_user") || "demo",
      event_id: o.event_id,
      market: o.market,
      selection: o.selection,
      stake: Number(stake),
      odds_at_bet: o.price,
    };

    try {
      setPlacingId(`${o.event_id}-${o.market}-${o.selection}`);
      const r = await placeBet(payload);
      alert("Bet placed: " + JSON.stringify(r));
      load(); // reload odds or bets
    } catch (e) {
      console.error(e);
      alert("Failed to place bet — check backend logs or network.");
    } finally {
      setPlacingId(null);
    }
  }

  return (
    <div>
      <h3>Live Odds (Mock Feed)</h3>

      <div style={{ marginBottom: 12 }}>
        <label>
          Stake:{" "}
          <input
            type="number"
            value={stake}
            min="0.01"
            step="0.1"
            onChange={(e) => setStake(e.target.value)}
            style={{ width: 100 }}
          />
        </label>
        <button onClick={load} style={{ marginLeft: 8 }}>
          Refresh
        </button>
      </div>

      {loading && <div>Loading…</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}

      <table border={1} cellPadding={8} style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Event</th>
            <th>Market</th>
            <th>Selection</th>
            <th>Price</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {odds.length === 0 && !loading && (
            <tr>
              <td colSpan={5}>No odds available</td>
            </tr>
          )}
          {odds.map((o) => (
            <tr key={`${o.event_id}-${o.market}-${o.selection}`}>
              <td>{o.event_id}</td>
              <td>{o.market}</td>
              <td>{o.selection}</td>
              <td>{o.price}</td>
              <td>
                <button
                  disabled={placingId === `${o.event_id}-${o.market}-${o.selection}`}
                  onClick={() => handleBet(o)}
                >
                  {placingId === `${o.event_id}-${o.market}-${o.selection}` ? "Placing..." : "Bet"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
