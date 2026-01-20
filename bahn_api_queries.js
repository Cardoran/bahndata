import axios from 'axios';
import { format, addDays, addHours } from 'date-fns';
import xml2js from 'xml2js';

export async function getTimetableXml(api_auth_headers, evaNr, date = null) {
  // If no date is provided, use the current date and time
  if (!date) {
    date = addHours(new Date(), 1);
  }

  // Format the date and hour as strings
  const dateString = format(date, 'yyMMdd');
  const hour = format(date, 'HH');

  // Construct the URL
  const url = `https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/${evaNr}/${dateString}/${hour}`;

  try {
    // Make the HTTP GET request
    const response = await axios.get(url, {
      headers: api_auth_headers,
    });

    // Log the URL for debugging
    console.log(response.config.url);

    // Handle specific HTTP status codes
    if (response.status === 410) {
      // If the response is 410 (Gone), retry with the next day
      return getTimetableXml(api_auth_headers, evaNr, addDays(date, 1));
    } else if (response.status === 401) {
      throw new Error("Code 401: Can't request timetable because the credentials are not correct. Please make sure that you are providing the correct credentials.");
    } else if (response.status === 400) {
      throw new Error("Code 400: Can't request timetable because the EVA number is not correct. Please make sure that you are providing the correct EVA number.");
    } else if (response.status !== 200) {
      throw new Error(`Can't request timetable! The request failed with the HTTP status code ${response.status}: ${response.statusText}`);
    }

    // Return the response text
    return await parseXml(response.data);
  } catch (error) {
    console.error('Error:', error.message);
    throw error;
  }
}

async function parseXml(xml) {
    try {
        const parser = new xml2js.Parser({ explicitArray: false });
        const result = await parser.parseStringPromise(xml);
        console.log('XML Result:', xml);
        console.log('JSON Result:', result);
        return result;
    } catch (error) {
        console.error('Error parsing XML:', error);
        throw error;
    }
}
