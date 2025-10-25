import React, { useEffect, useState } from 'react';
import OddsList from './components/OddsList';
import BetForm from './components/BetForm';
import { fetchOdds, placeBet } from './api';

function App() {
  const [odds, setOdds] = useState([]);
  const [selectedBet, setSelectedBet] = useState(null);

  useEffect(() => {
    fetchOdds().then(setOdds);

    // Poll every 30s
    const interval = setInterval(() => {
      fetchOdds().then(setOdds);
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const handlePlaceBet = async (bet) => {
    const result = await placeBet(bet);
    alert(`Bet placed! Status: ${result.status}`);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>SBK Engine</h1>
      <OddsList odds={odds} onSelect={(o) => setSelectedBet(o)} />
      {selectedBet && <BetForm selection={selectedBet} onSubmit={handlePlaceBet} />}
    </div>
  );
}

export default App;
