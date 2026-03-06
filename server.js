import { Pool } from 'pg';
import express from 'express';
import { miner_coordinator } from './miner.js';
import { pg_query_handler } from './pg_queries.js';
import apiHeaders from './auth.json' assert { type: 'json' };

const app = express();
const port = 80;

// Serve static files (e.g., HTML, CSS, JS)
app.use(express.static('public'));

// PostgreSQL connection pools
const stations_pool = new Pool({
  user: 'bahn_miner',
  host: '192.168.178.40',
  database: 'station_data',
  password: 'bahn_miner_password',
  port: 5432,
});
const timetable_pool = new Pool({
  user: 'bahn_miner',
  host: '192.168.178.40',
  database: 'departures_long_distance_stops',
  password: 'bahn_miner_password',
  port: 5432,
});

const stations_client = await stations_pool.connect();
const timetable_client = await timetable_pool.connect();
const pgq = new pg_query_handler(stations_client, timetable_client);
const miner = new miner_coordinator(apiHeaders, pgq);
miner.run_loop()

// Endpoint to trigger data fetch and store
app.get('/fetch-stations', async (req, res) => {
  // const client = await stations_pool.connect();
  try {
    const result = await stations_pool.query('SELECT * FROM stations LIMIT 10;')
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
    stations_pool.end(); // Close the PostgreSQL connection pool
    timetable_pool.end(); // Close the PostgreSQL connection pool
    process.exit(0);
  });
});
