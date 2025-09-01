import React from 'react';

const Home = ({ setCurrentPage }) => {
  return (
    <section className="text-center space-y-8">
      <div className="bg-gray-700 rounded-2xl p-6 shadow-lg">
        <h2 className="text-2xl font-bold text-gray-200 mb-4">Welcome to the Cricket Face-Off Predictor</h2>
        <p className="text-gray-300">
          This application uses data-driven simulations to predict outcomes of hypothetical cricket matchups. Explore the
          sections below to analyze player battles and team simulations across different formats.
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-gray-700 rounded-2xl p-6 shadow-lg transform transition-transform duration-300 hover:scale-105">
          <h3 className="text-xl font-semibold text-gray-200 mb-2">Player vs Player</h3>
          <p className="text-gray-400 mb-4">
            Simulate a face-off between a batsman and a bowler.
          </p>
          <button
            onClick={() => setCurrentPage('Hypothetical Matchups')}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded-xl transition duration-300"
          >
            Go to Matchups
          </button>
        </div>
        <div className="bg-gray-700 rounded-2xl p-6 shadow-lg transform transition-transform duration-300 hover:scale-105">
          <h3 className="text-xl font-semibold text-gray-200 mb-2">Team vs Team</h3>
          <p className="text-gray-400 mb-4">
            Build two custom XIs and simulate a full match.
          </p>
          <button
            onClick={() => setCurrentPage('Team vs Team')}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded-xl transition duration-300"
          >
            Go to Team Builder
          </button>
        </div>
        <div className="bg-gray-700 rounded-2xl p-6 shadow-lg transform transition-transform duration-300 hover:scale-105">
          <h3 className="text-xl font-semibold text-gray-200 mb-2">Player Insights</h3>
          <p className="text-gray-400 mb-4">
            Get a detailed AI-powered analysis of any player's career.
          </p>
          <button
            onClick={() => setCurrentPage('Player Insights')}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded-xl transition duration-300"
          >
            Get Insights
          </button>
        </div>
      </div>
    </section>
  );
};

export default Home;
