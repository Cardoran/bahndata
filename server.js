import { Pool } from 'pg';
import express from 'express';
import { miner_coordinator } from './miner.js';
import { pg_query_handler } from './pg_queries.js';

const app = express();
const port = 80;

// Serve static files (e.g., HTML, CSS, JS)
app.use(express.static('public'));

const apiHeaders = {
  'DB-Api-Key': '235a6da868e721b3ed0f8915d17759fb', // Replace with your API key
  'DB-Client-Id': '2b83a09f021fad54d68cc31e3b5e03e2',
  'Accept': 'application/json',
};

// PostgreSQL connection pool
const pool = new Pool({
  user: 'bahn_miner',
  host: '192.168.178.40',
  database: 'station_data',
  password: 'bahn_miner_password',
  port: 5432,
});

const client = await pool.connect();
const pgq = new pg_query_handler(client);
const miner = new miner_coordinator(apiHeaders, pgq);
miner.run()

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

// Start the server
const server = app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

// Handle SIGTERM for graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received. Shutting down gracefully...');
  server.close(() => {
    console.log('Server closed.');
    pool.end(); // Close the PostgreSQL connection pool
    process.exit(0);
  });
});
