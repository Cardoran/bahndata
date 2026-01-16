import axios from 'axios';
import { Pool } from 'pg';
import express from 'express';
import cron from 'node-cron';
import { insertStationData } from './pg_queries.js';

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

// API configuration
const apiUrl = 'https://apis.deutschebahn.com/db-api-marketplace/apis/station-data/v2/stations';
const apiHeaders = {
  'DB-Api-Key': '235a6da868e721b3ed0f8915d17759fb', // Replace with your API key
  'DB-Client-Id': '2b83a09f021fad54d68cc31e3b5e03e2',
  'Accept': 'application/json',
};

// Function to fetch data from the API
async function fetchStationData() {
  try {
    const response = await axios.get(apiUrl, { headers: apiHeaders });
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error.message);
    return null;
  }
}

// Function to store data in PostgreSQL
async function storeStationData(data) {
  const client = await pool.connect();
  try {
    // Insert data into the table
    for (const station of data.result) {
      await insertStationData(client, station);
    }
    console.log('Data stored successfully');
  } catch (error) {
    console.error('Error storing data:', error.message);
  } finally {
    client.release();
  }
}

// Endpoint to trigger data fetch and store
app.get('/fetch-stations', async (req, res) => {
  const client = await pool.connect();
  try {
    data = client.query('SELECT * FROM stations LIMIT 10;')
    res.send(data);
  } catch {
    res.send(error.message)
  }
  // const data = await fetchStationData();
  // if (data) {
  //   await storeStationData(data);
  //   res.send('Data fetched and stored successfully');
  // } else {
  //   res.status(500).send('Error fetching data');
  // }
  // res.send('joa, nüscht hier.')
});

// Call fetchStationData immediately when the server starts
(async () => {
  const data = await fetchStationData();
  if (data) {
    await storeStationData(data);
    console.log('Initial data fetch completed');
  }
})();

// Schedule data fetch every 5 hours
cron.schedule('0 */5 * * *', async () => {
  const data = await fetchStationData();
  if (data) {
    await storeStationData(data);
    console.log('Data fetched and stored automatically');
  }
});


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
