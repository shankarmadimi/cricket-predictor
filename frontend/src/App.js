import React, { useState } from 'react';
import Home from './components/Home';
import HypotheticalMatchups from './components/HypotheticalMatchups';
import TeamVsTeam from './components/TeamVsTeam';
import PlayerInsights from './components/PlayerInsights';
import About from './components/About';

const App = () => {
  const [currentPage, setCurrentPage] = useState('Home');

  const renderPage = () => {
    switch (currentPage) {
      case 'Home':
        return <Home setCurrentPage={setCurrentPage} />;
      case 'Hypothetical Matchups':
        return <HypotheticalMatchups />;
      case 'Team vs Team':
        return <TeamVsTeam />;
      case 'Player Insights':
        return <PlayerInsights />;
      case 'About':
        return <About />;
      default:
        return <Home setCurrentPage={setCurrentPage} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans flex flex-col items-center p-4 sm:p-8">
      <div className="w-full max-w-6xl bg-gray-800 rounded-3xl shadow-2xl p-6 sm:p-10">
        <header className="text-center mb-6">
          <h1 className="text-4xl sm:text-5xl font-extrabold text-blue-400 mb-2">
            Cricket Face-Off Predictor
          </h1>
          <p className="text-lg text-gray-400 mt-2">
            Predicting battles across generations
          </p>
        </header>
        <nav className="mb-8">
          <ul className="flex flex-wrap justify-center gap-2 sm:gap-4 font-semibold text-gray-300">
            {['Home', 'Hypothetical Matchups', 'Team vs Team', 'Player Insights', 'About'].map((page) => (
              <li key={page}>
                <button
                  onClick={() => setCurrentPage(page)}
                  className={`py-2 px-4 rounded-full transition-colors ${currentPage === page ? 'bg-blue-600 text-white shadow-lg' : 'bg-gray-700 hover:bg-gray-600'}`}
                >
                  {page}
                </button>
              </li>
            ))}
          </ul>
        </nav>
        <main className="space-y-12">
          {renderPage()}
        </main>
      </div>
    </div>
  );
};

export default App;
