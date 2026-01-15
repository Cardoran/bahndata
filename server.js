import axios from 'axios';
import { Pool } from 'pg';
import express from 'express';
import cron from 'node-cron';
import { insertStationData } from './pg_queries.js';

const app = express();
const port = 80;


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
    // Create a table if it doesn't exist
    // await client.query(`
    //   CREATE TABLE IF NOT EXISTS stations (
    //     id SERIAL PRIMARY KEY,
    //     station_id VARCHAR(50),
    //     station_name VARCHAR(255),
    //     data JSONB,
    //     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    //   )
    // `);
    var i = 0;
    console.log("try");
    // Insert data into the table
    for (const station of data.result) {
      console.log("await", i, station.name, station.municipality_code, station.has_mobility_service, station.has_stepless_access);
      i++;
      if(i>10){
        break;
      }
      await insertStationData(client, station);
      // await client.query(
      //   'INSERT INTO stations (station_id, station_name, data) VALUES ($1, $2, $3) ON CONFLICT (station_id) DO NOTHING',
      //   [station.id, station.name, station]
      // );
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
  const data = await fetchStationData();
  if (data) {
    await storeStationData(data);
    res.send('Data fetched and stored successfully');
  } else {
    res.status(500).send('Error fetching data');
  }
});

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
