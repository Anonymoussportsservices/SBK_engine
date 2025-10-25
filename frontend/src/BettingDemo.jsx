import React, { useEffect, useState } from "react";
import { fetchOdds, placeBet } from "./api";

export default function BettingDemo() {
  const [odds, setOdds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  // Fetch odds on component mount
  useEffect(() => {
    async function loadOdds() {
      try {
        const data = await fetchOdds();
        setOdds(data);
      } catch (err) {
        setMessage(`Error fetching odds: ${err.message}`);
      } finally {
        setLoading(false);
      }
    }
    loadOdds();
  }, []);

  // Test bet function
  async function testBet(selection) {
    const betPayload = {
      user_id: 1,
      event_id: selection.event_id,
      market: selection.market,
      selection: selection.selection,
      stake: 10,
      odds_at_bet: selection.price,
    };
    try {
      const result = await placeBet(betPayload);
      setMessage(`Bet placed! ID: ${result.id}, Status: ${result.status}`);
    } catch (err) {
      setMessage(`Error placing bet: ${err.message}`);
    }
  }

  if (loading) return <p>Loading odds...</p>;

  return (
    <div>
      <h2>Live Odds</h2>
      {message && <p>{message}</p>}
      <ul>
        {odds.map((o, idx) => (
          <li key={idx}>
            {o.event_id} - {o.market} - {o.selection}: {o.price}{" "}
            <button onClick={() => testBet(o)}>Bet $10</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
