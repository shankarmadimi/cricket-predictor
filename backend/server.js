const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.post('/api/simulate/player-vs-player', async (req, res) => {
    try {
        const { player1, player2 } = req.body;
        if (!player1 || !player2) {
            return res.status(400).json({ error: 'Please select both players.' });
        }
        const winner = Math.random() > 0.5 ? player1 : player2;
        const probability = (Math.random() * 20 + 70).toFixed(2);
        const pythonProcess = spawn('python3', [
            'ml_model/predictor.py',
            'generate_reasoning',
            JSON.stringify({ winner, opponent: winner === player1 ? player2 : player1, probability, type: 'player' })
        ]);

        let reasoning = '';
        pythonProcess.stdout.on('data', (data) => {
            reasoning += data.toString();
        });
        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python Error: ${data.toString()}`);
        });
        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                return res.status(500).json({ error: 'Failed to generate reasoning.' });
            }
            res.json({
                winner,
                probability: `${probability}%`,
                reasoning: reasoning.trim() || "No specific reasoning available.",
            });
        });
    } catch (error) {
        console.error('Error during player simulation:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.post('/api/simulate/team-vs-team', async (req, res) => {
    try {
        const { team1, team2 } = req.body;
        if (!team1 || team1.length !== 11 || !team2 || team2.length !== 11) {
            return res.status(400).json({ error: 'Each team must have exactly 11 players.' });
        }
        const winner = Math.random() > 0.5 ? 'Team 1' : 'Team 2';
        const probability = (Math.random() * 20 + 70).toFixed(2);
        const pythonProcess = spawn('python3', [
            'ml_model/predictor.py',
            'generate_reasoning',
            JSON.stringify({ winner, teams: { team1, team2 }, probability, type: 'team' })
        ]);

        let reasoning = '';
        pythonProcess.stdout.on('data', (data) => {
            reasoning += data.toString();
        });
        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python Error: ${data.toString()}`);
        });
        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                return res.status(500).json({ error: 'Failed to generate reasoning.' });
            }
            res.json({
                winner,
                probability: `${probability}%`,
                reasoning: reasoning.trim() || "No specific reasoning available.",
            });
        });
    } catch (error) {
        console.error('Error during team simulation:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.post('/api/player-insights', async (req, res) => {
    try {
        const { player } = req.body;
        if (!player) {
            return res.status(400).json({ error: 'Please provide a player name.' });
        }
        const pythonProcess = spawn('python3', [
            'ml_model/predictor.py',
            'generate_insights',
            player
        ]);

        let insights = '';
        pythonProcess.stdout.on('data', (data) => {
            insights += data.toString();
        });
        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python Error: ${data.toString()}`);
        });
        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                return res.status(500).json({ error: 'Failed to generate insights.' });
            }
            res.json({
                insight: insights.trim() || "Could not generate insights for this player."
            });
        });
    } catch (error) {
        console.error('Error generating player insights:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
