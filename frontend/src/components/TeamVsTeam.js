import React, { useState } from 'react';

const TeamVsTeam = () => {
  const [teams, setTeams] = useState({
    team1: [],
    team2: [],
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const mockAllPlayers = [
    'Virat Kohli', 'Rohit Sharma', 'Jasprit Bumrah', 'Sachin Tendulkar', 'Shane Warne', 'Wasim Akram', 'Chris Gayle',
    'Ben Stokes', 'AB de Villiers', 'MS Dhoni', 'Mitchell Starc', 'Dale Steyn', 'Rashid Khan', 'Babar Azam'
  ];

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleAddPlayer = (player, teamKey) => {
    if (teams[teamKey].length < 11) {
      setTeams(prevTeams => ({
        ...prevTeams,
        [teamKey]: [...prevTeams[teamKey], player],
      }));
    }
  };

  const handleRemovePlayer = (player, teamKey) => {
    setTeams(prevTeams => ({
      ...prevTeams,
      [teamKey]: prevTeams[teamKey].filter(p => p !== player),
    }));
  };

  const handleSimulateMatch = async () => {
    if (teams.team1.length !== 11 || teams.team2.length !== 11) {
      setResult({ message: "Both teams must have exactly 11 players." });
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/simulate/team-vs-team', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ team1: teams.team1, team2: teams.team2 }),
      });

      const data = await response.json();
      if (response.ok) {
        setResult({
          message: `The match is predicted to be won by ${data.winner}.`,
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

  const filteredPlayers = mockAllPlayers.filter(player =>
    player.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getBackgroundColor = (prob) => {
    const percentage = parseFloat(prob);
    if (percentage > 85) return 'bg-green-600';
    if (percentage > 75) return 'bg-yellow-600';
    return 'bg-red-600';
  };

  const isSimulateDisabled = teams.team1.length !== 11 || teams.team2.length !== 11 || loading;

  return (
    <section className="bg-gray-700 rounded-2xl p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-gray-200 mb-4 flex items-center">
        <span className="mr-2">🏆</span> Custom XI vs Custom XI
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Available Players Column */}
        <div className="bg-gray-800 rounded-xl p-4 shadow-inner md:col-span-1">
          <h3 className="text-xl font-semibold text-gray-200 mb-4">Available Players</h3>
          <input
            type="text"
            placeholder="Search for a player..."
            value={searchTerm}
            onChange={handleSearch}
            className="w-full bg-gray-700 text-gray-200 border-none rounded-lg p-2 mb-4 focus:ring focus:ring-blue-500 focus:outline-none"
          />
          <div className="space-y-2 max-h-96 overflow-y-auto custom-scrollbar pr-2">
            {filteredPlayers.map(player => (
              <div key={player} className="bg-gray-700 text-gray-300 p-2 rounded-lg flex justify-between items-center transition-transform duration-200 hover:scale-[1.02]">
                <span>{player}</span>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleAddPlayer(player, 'team1')}
                    disabled={teams.team1.length >= 11 || teams.team1.includes(player)}
                    className="bg-blue-500 hover:bg-blue-600 text-white font-semibold text-xs px-2 py-1 rounded-full disabled:bg-gray-500 disabled:cursor-not-allowed"
                  >
                    Add to T1
                  </button>
                  <button
                    onClick={() => handleAddPlayer(player, 'team2')}
                    disabled={teams.team2.length >= 11 || teams.team2.includes(player)}
                    className="bg-green-500 hover:bg-green-600 text-white font-semibold text-xs px-2 py-1 rounded-full disabled:bg-gray-500 disabled:cursor-not-allowed"
                  >
                    Add to T2
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Team 1 Column */}
        <div className="bg-gray-800 rounded-xl p-4 shadow-inner md:col-span-1">
          <h3 className="text-xl font-semibold text-gray-200 mb-4 flex justify-between items-center">
            Team 1 <span className="text-blue-400 font-bold">{teams.team1.length}/11</span>
          </h3>
          <div className="space-y-2 max-h-96 overflow-y-auto custom-scrollbar pr-2">
            {teams.team1.length === 0 ? (
              <p className="text-gray-500 italic text-center py-4">Add players to Team 1</p>
            ) : (
              teams.team1.map(player => (
                <div key={player} className="bg-blue-900 text-blue-100 p-2 rounded-lg flex justify-between items-center transition-transform duration-200 hover:scale-[1.02]">
                  <span>{player}</span>
                  <button
                    onClick={() => handleRemovePlayer(player, 'team1')}
                    className="bg-blue-500 hover:bg-blue-600 text-white text-xs px-2 py-1 rounded-full"
                  >
                    Remove
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Team 2 Column */}
        <div className="bg-gray-800 rounded-xl p-4 shadow-inner md:col-span-1">
          <h3 className="text-xl font-semibold text-gray-200 mb-4 flex justify-between items-center">
            Team 2 <span className="text-green-400 font-bold">{teams.team2.length}/11</span>
          </h3>
          <div className="space-y-2 max-h-96 overflow-y-auto custom-scrollbar pr-2">
            {teams.team2.length === 0 ? (
              <p className="text-gray-500 italic text-center py-4">Add players to Team 2</p>
            ) : (
              teams.team2.map(player => (
                <div key={player} className="bg-green-900 text-green-100 p-2 rounded-lg flex justify-between items-center transition-transform duration-200 hover:scale-[1.02]">
                  <span>{player}</span>
                  <button
                    onClick={() => handleRemovePlayer(player, 'team2')}
                    className="bg-green-500 hover:bg-green-600 text-white text-xs px-2 py-1 rounded-full"
                  >
                    Remove
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
      <button
        onClick={handleSimulateMatch}
        disabled={isSimulateDisabled}
        className="w-full mt-8 bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 rounded-xl transition duration-300 ease-in-out transform hover:scale-105 shadow-xl disabled:bg-gray-500 disabled:cursor-not-allowed"
      >
        {loading ? 'Simulating...' : 'Simulate Match'}
      </button>
      {result && (
        <div className="bg-gray-800 rounded-lg p-4 mt-8">
          <h3 className="text-xl font-semibold text-gray-200 mb-2">Match Prediction</h3>
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

export default TeamVsTeam;
