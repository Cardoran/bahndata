import { Pool } from 'pg';
import express from 'express';
import { miner_loop } from './miner.js';

const app = express();
const port = 80;

// Serve static files (e.g., HTML, CSS, JS)
app.use(express.static('public'));

// PostgreSQL connection pool
const pool = new Pool({
  user: 'bahn_miner',
  host: '192.168.178.40',
  database: 'station_data',
  password: 'bahn_miner_password',
  port: 5432,
});


// Endpoint to trigger data fetch and store
app.get('/fetch-stations', async (req, res) => {
  // const client = await pool.connect();
  try {
    const result = await pool.query('SELECT * FROM stations LIMIT 10;')
    res.json(result.rows);
  } catch (error) {
    res.send(error.message);
  }
});

app.get('/timetable', async (req, res) => {
  // const response = await getTimetableXml(apiHeaders, 8000068);
  // res.json(response);
});

miner_loop();

// Handle SIGTERM for graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received. Shutting down gracefully...');
  app.close(() => {
    console.log('Server closed.');
    pool.end(); // Close the PostgreSQL connection pool
    process.exit(0);
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
