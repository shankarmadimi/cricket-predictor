import React from 'react';

const About = () => {
  return (
    <section className="bg-gray-700 rounded-2xl p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-gray-200 mb-4">About This Project</h2>
      <div className="text-gray-400 space-y-4">
        <p>
          The Cricket Face-Off Predictor is a data-driven simulation project designed to provide an objective way to settle
          the age-old debates of cricket. It leverages a combination of web development, data analysis, and machine learning
          to simulate hypothetical matchups between players and teams from different eras.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="text-xl font-semibold text-gray-200 mb-2">Methodology</h3>
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Data from public sources (Cricsheet, Kaggle)</li>
              <li>Monte Carlo simulations for realistic outcomes</li>
              <li>Regression models to predict player performance</li>
              <li>AI-powered reasoning for insightful predictions</li>
            </ul>
          </div>
          <div>
            <h3 className="text-xl font-semibold text-gray-200 mb-2">Tech Stack</h3>
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Frontend: React.js & Tailwind CSS</li>
              <li>Backend: Node.js (Express)</li>
              <li>Machine Learning: Python (Pandas, Scikit-learn)</li>
              <li>AI: Gemini API for dynamic text generation</li>
            </ul>
          </div>
        </div>
        <p className="mt-4">
          This project blends a passion for sports with technology, providing a fun and insightful tool for cricket fans,
          fantasy cricket players, and data enthusiasts alike.
        </p>
      </div>
    </section>
  );
};

export default About;
