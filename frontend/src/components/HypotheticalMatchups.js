import React, { useState } from 'react';

const HypotheticalMatchups = () => {
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ballType, setBallType] = useState('');

  const mockPlayers = ['Virat Kohli', 'Jasprit Bumrah', 'Sachin Tendulkar', 'Shane Warne', 'Wasim Akram', 'Chris Gayle'];

  const getBackgroundColor = (prob) => {
    const percentage = parseFloat(prob);
    if (percentage > 85) return 'bg-green-600';
    if (percentage > 75) return 'bg-yellow-600';
    return 'bg-red-600';
  };

  const handlePlayerSimulation = async (e) => {
    e.preventDefault();
    if (!player1 || !player2 || !ballType) {
      setResult({ message: "Please select both players and the ball type." });
      return;
    }
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/simulate/player-vs-player', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player1, player2, ballType }),
      });

      const data = await response.json();
      if (response.ok) {
        setResult({
          message: `The face-off between ${player1} and ${player2} is predicted to be won by ${data.winner}.`,
          details: data,
        });
      } else {
        setResult({ message: data.error });
      }
    } catch (error) {
      setResult({ message: "An error occurred during simulation. Please check the server." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="bg-gray-700 rounded-2xl p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-gray-200 mb-4 flex items-center">
        <span className="mr-2">🏏</span> Player vs Player
      </h2>
  <form onSubmit={handlePlayerSimulation} className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1 text-gray-300" htmlFor="player1">Select a Batter</label>
          <select
            id="player1"
            value={player1}
            onChange={(e) => setPlayer1(e.target.value)}
            className="bg-gray-600 text-gray-200 border-none rounded-lg p-2 focus:ring focus:ring-blue-500 focus:outline-none"
          >
            <option value="">Select a Player</option>
            {mockPlayers.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1 text-gray-300" htmlFor="player2">Select a Bowler</label>
          <select
            id="player2"
            value={player2}
            onChange={(e) => setPlayer2(e.target.value)}
            className="bg-gray-600 text-gray-200 border-none rounded-lg p-2 focus:ring focus:ring-blue-500 focus:outline-none"
          >
            <option value="">Select a Player</option>
            {mockPlayers.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1 text-gray-300" htmlFor="ballType">Select Ball Type</label>
          <select
            id="ballType"
            value={ballType}
            onChange={(e) => setBallType(e.target.value)}
            className="bg-gray-600 text-gray-200 border-none rounded-lg p-2 focus:ring focus:ring-blue-500 focus:outline-none"
          >
            <option value="">Select Ball Type</option>
            <option value="red">Red Ball</option>
            <option value="white">White Ball</option>
          </select>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="col-span-1 sm:col-span-3 mt-4 bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 rounded-xl transition duration-300 ease-in-out transform hover:scale-105 shadow-md disabled:bg-gray-500 disabled:cursor-not-allowed"
        >
          {loading ? 'Simulating...' : 'Simulate Player Battle'}
        </button>
      </form>
      {result && (
        <div className="bg-gray-800 rounded-lg p-4 mt-8">
          <h3 className="text-xl font-semibold text-gray-200 mb-2">Prediction Results</h3>
          <p className="text-lg text-gray-200 font-semibold mb-2">{result.message}</p>
          {result.details && (
            <div className="mt-4 space-y-3">
              <div className="flex items-center text-gray-300">
                <span className="font-bold mr-2">Winner:</span> {result.details.winner}
              </div>
              <div className="flex items-center text-gray-300">
                <span className="font-bold mr-2">Probability:</span>
                <span className={`px-2 py-1 rounded-full text-white font-bold text-xs ${getBackgroundColor(result.details.probability)}`}>
                  {result.details.probability}
                </span>
              </div>
              <div>
                <span className="font-bold text-gray-300 block mb-1">Reasoning:</span>
                <p className="text-sm text-gray-400 italic">{result.details.reasoning}</p>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
};

export default HypotheticalMatchups;
