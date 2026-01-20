import axios from 'axios';
import cron from 'node-cron';
import { getTimetableXml } from './bahn_api_queries.js';

function timestamp() {
    const now = new Date();
    const timestamp = now.toLocaleString(); // or use a custom format
    return `[${timestamp}]`;
}

export class miner_coordinator {
    constructor(apiHeaders, pg_query_handler) {
        // API configuration
        this.apiHeaders = apiHeaders;
        this.apiUrl_stations = 'https://apis.deutschebahn.com/db-api-marketplace/apis/station-data/v2/stations';
        this.pgq = pg_query_handler;
    }

    run () {
        this.miner_loop(21);

        // Call fetchStationData immediately when the server starts
        this.refresh_station_data();

        // Schedule data fetch every 5 hours
        cron.schedule('0 4 * * *', this.refresh_station_data);
    }

    run_loop () {
        cron.schedule('0 * * * *', async () => {
            this.miner_loop(20);
        });
    }
    
    async miner_loop(time) {
        const eva_list = get_station_evas();
        const l = length(eva_list);
        var i = 0;
        const intervalId = setInterval(async () => {
            const tt = await this.get_timetable(eva_list[i], time);
            this.pgq.store_timetable(tt);
            i ++;
            if (i>=l) {
                console.log('done all evas');
                clearInterval(intervalId); 
            }
        }, 1200);
    }
    async get_timetable(station, time) {
        console.log(timestamp(), "api query:", station, time);
        return "dummy data";
    }
    
    async refresh_station_data() {
        const data = await this.fetchStationData();
        if (data) {
            await this.pgq.storeStationData(data);
            console.log('Data fetched and stored automatically');
        }
    }
    // Function to fetch data from the API
    async fetchStationData() {
        try {
            const response = await axios.get(this.apiUrl_stations, { headers: this.apiHeaders });
            return response.data;
        } catch (error) {
            console.error('Error fetching data:', error.message);
            return null;
        }
    }

}

