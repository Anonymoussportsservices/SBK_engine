import React, { useState } from 'react';

export default function BetForm({ selection, onSubmit }) {
  const [stake, setStake] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      user_id: 1, // placeholder
      event_id: selection.event_id,
      market: selection.market,
      selection: selection.selection,
      stake,
      odds_at_bet: selection.price,
    });
    setStake('');
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
      <h3>Place Bet on {selection.selection}</h3>
      <input
        type="number"
        value={stake}
        onChange={(e) => setStake(e.target.value)}
        placeholder="Stake"
        required
      />
      <button type="submit">Place Bet</button>
    </form>
  );
}
