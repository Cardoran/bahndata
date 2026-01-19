import axios from 'axios';
import cron from 'node-cron';
import { insertStationData } from './pg_queries.js';
import { getTimetableXml } from './bahn_api_queries.js';

function timestamp() {
    const now = new Date();
    const timestamp = now.toLocaleString(); // or use a custom format
    return `[${timestamp}]`;
  }

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

// Call fetchStationData immediately when the server starts
// (async () => {
//   const data = await fetchStationData();
//   if (data) {
//     await storeStationData(data);
//     console.log('Initial data fetch completed');
//   }
// })();

// Schedule data fetch every 5 hours
cron.schedule('0 */5 * * *', async () => {
    const data = await fetchStationData();
    if (data) {
      await storeStationData(data);
      console.log('Data fetched and stored automatically');
    }
});

async function get_timetable(station, time) {
    console.log(timestamp(), "api query:", station, time);
    return "dummy data";
}

async function store_timetable(tt) {
    console.log(timestamp(), "db store data", tt);
}

async function miner_loop(time) {
    const intervalId = setInterval(async () => {
        const tt = await get_timetable(8000068, time);
        store_timetable(tt);
    }, 1200);
}

export async function miner_coordinator() {
    miner_loop(21);
    // cron.schedule('0 * * * *', async () => {
    //     miner_loop(20);
    // });
}