import React from 'react';

export default function OddsList({ odds, onSelect }) {
  if (!odds.length) return <p>No odds available</p>;

  return (
    <div>
      <h2>Live Odds</h2>
      <table border="1" cellPadding="8">
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
          {odds.map((o, idx) => (
            <tr key={idx}>
              <td>{o.event_id}</td>
              <td>{o.market}</td>
              <td>{o.selection}</td>
              <td>{o.price}</td>
              <td>
                <button onClick={() => onSelect(o)}>Bet</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
