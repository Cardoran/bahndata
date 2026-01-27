export class pg_query_handler {
    constructor (stations_client, timetable_client) {
        this.st_client = stations_client;
        this.tt_client = timetable_client;
    }

    async insertStationData(stationData) {
        // const client = await pool.connect();
    
        try {
            await this.st_client.query('BEGIN');
        
            // Insert mailing address (handle conflict on city, street, zipcode)
            const mailingAddressResult = await this.st_client.query(
                `INSERT INTO mailing_addresses (city, zipcode, street)
                 VALUES ($1, $2, $3)
                 ON CONFLICT (city, street, zipcode)
                 DO UPDATE SET city = EXCLUDED.city, street = EXCLUDED.street, zipcode = EXCLUDED.zipcode
                 RETURNING id`,
                [stationData.mailingAddress.city, stationData.mailingAddress.zipcode, stationData.mailingAddress.street]
            );
            const mailingAddressId = mailingAddressResult.rows[0].id;
        
            // Insert regional area (handle conflict on number)
            const regionalAreaResult = await this.st_client.query(
                `INSERT INTO regional_areas (number, name, short_name)
                 VALUES ($1, $2, $3)
                 ON CONFLICT (number)
                 DO UPDATE SET name = EXCLUDED.name, short_name = EXCLUDED.short_name
                 RETURNING id`,
                [stationData.regionalbereich.number, stationData.regionalbereich.name, stationData.regionalbereich.shortName]
            );
            const regionalAreaId = regionalAreaResult.rows[0].id;
        
            // Insert task carrier (handle conflict on short_name)
            const taskCarrierResult = await this.st_client.query(
                `INSERT INTO task_carriers (short_name, name)
                 VALUES ($1, $2)
                 ON CONFLICT (short_name)
                 DO UPDATE SET name = EXCLUDED.name
                 RETURNING id`,
                [stationData.aufgabentraeger.shortName, stationData.aufgabentraeger.name]
            );
            const taskCarrierId = taskCarrierResult.rows[0].id;
        
            // Insert time table office (handle conflict on email)
            const timeTableOfficeResult = await this.st_client.query(
                `INSERT INTO time_table_offices (email, name)
                 VALUES ($1, $2)
                 ON CONFLICT (name)
                 DO UPDATE SET email = EXCLUDED.email
                 RETURNING id`,
                [stationData.timeTableOffice.email, stationData.timeTableOffice.name]
            );
            const timeTableOfficeId = timeTableOfficeResult.rows[0].id;
        
            // Insert SZentrale (handle conflict on number)
            const szentraleResult = await this.st_client.query(
                `INSERT INTO szentrale (number, public_phone_number, name)
                 VALUES ($1, $2, $3)
                 ON CONFLICT (number)
                 DO UPDATE SET public_phone_number = EXCLUDED.public_phone_number, name = EXCLUDED.name
                 RETURNING id`,
                [stationData.szentrale.number, stationData.szentrale.publicPhoneNumber, stationData.szentrale.name]
            );
            const szentraleId = szentraleResult.rows[0].id;
        
            // Insert station management (handle conflict on number)
            const stationManagementResult = await this.st_client.query(
                `INSERT INTO station_management (number, name)
                 VALUES ($1, $2)
                 ON CONFLICT (number)
                 DO UPDATE SET name = EXCLUDED.name
                 RETURNING id`,
                [stationData.stationManagement.number, stationData.stationManagement.name]
            );
            const stationManagementId = stationManagementResult.rows[0].id;
        
            // Insert station (handle conflict on number)
            const stationResult = await this.st_client.query(
                `INSERT INTO stations (
                    number, ifopt, name, category, price_category, has_parking, has_bicycle_parking,
                    has_local_public_transport, has_public_facilities, has_locker_system, has_taxi_rank,
                    has_travel_necessities, has_stepless_access, has_mobility_service, has_wifi,
                    has_travel_center, has_railway_mission, has_db_lounge, has_lost_and_found, has_car_rental,
                    federal_state, federal_state_code, country_code, municipality_code, mailing_address_id,
                    regional_area_id, task_carrier_id, time_table_office_id, szentrale_id, station_management_id
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20,
                        $21, $22, $23, $24, $25, $26, $27, $28, $29, $30)
                ON CONFLICT (number) DO UPDATE SET
                    ifopt = EXCLUDED.ifopt,
                    name = EXCLUDED.name,
                    category = EXCLUDED.category,
                    price_category = EXCLUDED.price_category,
                    has_parking = EXCLUDED.has_parking,
                    has_bicycle_parking = EXCLUDED.has_bicycle_parking,
                    has_local_public_transport = EXCLUDED.has_local_public_transport,
                    has_public_facilities = EXCLUDED.has_public_facilities,
                    has_locker_system = EXCLUDED.has_locker_system,
                    has_taxi_rank = EXCLUDED.has_taxi_rank,
                    has_travel_necessities = EXCLUDED.has_travel_necessities,
                    has_stepless_access = EXCLUDED.has_stepless_access,
                    has_mobility_service = EXCLUDED.has_mobility_service,
                    has_wifi = EXCLUDED.has_wifi,
                    has_travel_center = EXCLUDED.has_travel_center,
                    has_railway_mission = EXCLUDED.has_railway_mission,
                    has_db_lounge = EXCLUDED.has_db_lounge,
                    has_lost_and_found = EXCLUDED.has_lost_and_found,
                    has_car_rental = EXCLUDED.has_car_rental,
                    federal_state = EXCLUDED.federal_state,
                    federal_state_code = EXCLUDED.federal_state_code,
                    country_code = EXCLUDED.country_code,
                    municipality_code = EXCLUDED.municipality_code,
                    mailing_address_id = EXCLUDED.mailing_address_id,
                    regional_area_id = EXCLUDED.regional_area_id,
                    task_carrier_id = EXCLUDED.task_carrier_id,
                    time_table_office_id = EXCLUDED.time_table_office_id,
                    szentrale_id = EXCLUDED.szentrale_id,
                    station_management_id = EXCLUDED.station_management_id
                RETURNING id`,
                [
                    stationData.number, stationData.ifopt, stationData.name, stationData.category,
                    stationData.priceCategory, stationData.hasParking, stationData.hasBicycleParking,
                    stationData.hasLocalPublicTransport, stationData.hasPublicFacilities, stationData.hasLockerSystem,
                    stationData.hasTaxiRank, stationData.hasTravelNecessities, stationData.hasSteplessAccess,
                    stationData.hasMobilityService, stationData.hasWiFi, stationData.hasTravelCenter,
                    stationData.hasRailwayMission, stationData.hasDBLounge, stationData.hasLostAndFound,
                    stationData.hasCarRental, stationData.federalState, stationData.federalStateCode,
                    stationData.countryCode, stationData.municipalityCode, mailingAddressId, regionalAreaId,
                    taskCarrierId, timeTableOfficeId, szentraleId, stationManagementId
                ]
            );
            const stationId = stationResult.rows[0].id;
        
            // Insert EVA numbers (handle conflict on station_id and number)
            for (const evaNumber of stationData.evaNumbers) {
                await this.st_client.query(
                    `INSERT INTO eva_numbers (station_id, number, is_main, latitude, longitude)
                     VALUES ($1, $2, $3, $4, $5)
                     ON CONFLICT (number)
                     DO UPDATE SET is_main = EXCLUDED.is_main, latitude = EXCLUDED.latitude, longitude = EXCLUDED.longitude`,
                    [stationId, evaNumber.number, evaNumber.isMain, evaNumber.geographicCoordinates.coordinates[1], evaNumber.geographicCoordinates.coordinates[0]]
                );
            }
        
            // Insert RIL100 identifiers (handle conflict on station_id and ril_identifier)
            for (const ril100 of stationData.ril100Identifiers) {
                await this.st_client.query(
                    `INSERT INTO ril100_identifiers (
                        station_id, ril_identifier, is_main, has_steam_permission, steam_permission,
                        latitude, longitude, primary_location_code
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (ril_identifier)
                    DO UPDATE SET
                        station_id = EXCLUDED.station_id,
                        is_main = EXCLUDED.is_main,
                        has_steam_permission = EXCLUDED.has_steam_permission,
                        steam_permission = EXCLUDED.steam_permission,
                        latitude = EXCLUDED.latitude,
                        longitude = EXCLUDED.longitude,
                        primary_location_code = EXCLUDED.primary_location_code`,
                    [
                        stationId, ril100.rilIdentifier, ril100.isMain, ril100.hasSteamPermission,
                        ril100.steamPermission, ril100.geographicCoordinates?.coordinates?.[1] ?? null,
                        ril100.geographicCoordinates?.coordinates?.[0] ?? null, ril100.primaryLocationCode
                    ]
                );
            }
        
            await this.st_client.query('COMMIT');
        } catch (error) {
            await this.st_client.query('ROLLBACK');
            console.error('Error inserting data:', error);
            throw error;
        } finally {
            // this.st_client.release();
        }
    }

    // Function to store station data in PostgreSQL
    async storeStationData(data) {
        // const client = await pool.connect();
        try {
        // Insert data into the table
            for (const station of data.result) {
                await this.insertStationData(station);
            }
            console.log('Data stored successfully');
        } catch (error) {
            console.error('Error storing data:', error.message);
        } finally {
            // this.st_client.release();
        }
    }
    
    async store_timetable(tt_data) {
        console.log("db store data", tt_data);
        console.log("db store data", tt_data.timetable.station);
        try {
            await this.tt_client.query('BEGIN');
        
            // Insert station eva and name (handle conflict on station_name)
            const station_result = await this.tt_client.query(
                `INSERT INTO stations (station_name)
                 VALUES ($1)
                 ON CONFLICT (station_name)
                 DO NOTHING
                 RETURNING id`,
                [tt_data.timetable.station]
            );
            const station_id = station_result.rows[0].id;
            console.log("stored data to:", station_id);

            await this.tt_client.query('COMMIT');
        } catch (error) {
            await this.tt_client.query('ROLLBACK');
            console.error('Error inserting data:', error);
            throw error;
        } finally {
            // this.tt_client.release();
        }
    }

    // pulls from database

    async get_station_evas(min_category, max_category) {
        if (!max_category) {
            max_category = 5
        }
        try{
            const result = await this.st_client.query(`select 
                (select en.number 
                from eva_numbers en 
                where en.station_id = s.id and en.is_main is true 
                limit 1) as eva 
                from stations s 
                where category <= 5;`);//[8080040, 8000452, 8000473]
            return result.rows.map(row => row.eva);
        }
        catch (error) {
            console.error('Error getting evas from database', error.message);
        }
    }
}