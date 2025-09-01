import React, { useState } from 'react';

const PlayerInsights = () => {
  const [selectedPlayer, setSelectedPlayer] = useState('');
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);

  const mockPlayers = ['Virat Kohli', 'Jasprit Bumrah', 'Sachin Tendulkar', 'Shane Warne', 'Wasim Akram', 'Chris Gayle'];

  const handleGetInsight = async () => {
    if (!selectedPlayer) {
      setInsight({ message: "Please select a player." });
      return;
    }
    setLoading(true);
    setInsight(null);
    try {
      const response = await fetch('http://localhost:5000/api/insights/player', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player: selectedPlayer }),
      });
      const data = await response.json();
      if (response.ok) {
        setInsight({
          name: selectedPlayer,
          biography: data.biography,
        });
      } else {
        setInsight({ message: data.error });
      }
    } catch (error) {
      setInsight({ message: "An error occurred fetching insights. Please check the server." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="bg-gray-700 rounded-2xl p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-gray-200 mb-4 flex items-center">
        <span className="mr-2">📈</span> Player Insights
      </h2>
      <div className="flex flex-col sm:flex-row sm:items-end gap-4 mb-6">
        <div className="flex-grow">
          <label className="text-sm font-medium mb-1 text-gray-300" htmlFor="player-select">Select a Player</label>
          <select
            id="player-select"
            value={selectedPlayer}
            onChange={(e) => setSelectedPlayer(e.target.value)}
            className="w-full bg-gray-600 text-gray-200 border-none rounded-lg p-2 focus:ring focus:ring-blue-500 focus:outline-none"
          >
            <option value="">Select a Player</option>
            {mockPlayers.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>
        <button
          onClick={handleGetInsight}
          disabled={!selectedPlayer || loading}
          className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded-xl transition duration-300 ease-in-out transform hover:scale-105 shadow-md disabled:bg-gray-500 disabled:cursor-not-allowed"
        >
          {loading ? 'Generating...' : 'Get AI Insights'}
        </button>
      </div>
      {insight && (
        <div className="bg-gray-800 rounded-lg p-4 mt-8">
          <h3 className="text-xl font-semibold text-gray-200 mb-2">{insight.name}</h3>
          <div className="text-gray-400 text-sm leading-relaxed space-y-4">
            {insight.biography.split('\n').map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
          </div>
        </div>
      )}
    </section>
  );
};

export default PlayerInsights;
