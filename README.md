# Bahndata
Bahndata is a simple node.js server that queries the public deutschebahn API for the timetable of the stations tier 5 and below. The data is stored in a PostgreSQL database which can be set up with the commands in the `/postgre` folder.

For the queries to be executed, a DB-API Client-Id and Api-Key pair is required which needs to be provided in a auth.json file with the following format in the main directory before building the container:
```
{
"DB-Api-Key": "xxxx",
"DB-Client-Id": "yyyy",
"Accept": "application/json"
}
```
## functionality
The server performs a loop over all tier 5 and below stations (approx. 2000) every hour with the individual queries spaced evenly across approximately 40 minutes. This is done to keep below the limit of 60 queries per minute or 3600 per hour.
The data received is then saved into a PostgreSQL database (some of the more uncommonly appearing fields are not implemented yet) where it can then be queried for further analysis.
## TODO
- querying the delay data of the timetables
- storing the delay data into the database
- providing an interface (possibly in a separate repo) to view the database and perform some standard analysis on it, e.g.
	- time-based connection spider
	- changeover-based connection spider
	- seeking connections and all alternatives (other than what the DB App provides)
	- delay statistics (similar to David Kriesel's CCC talk)
		- delay prognosis (for when I want to travel a certain route or change at a certain station)
- some surveillance tool to check the status of the miner and storage capacity
