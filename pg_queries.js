const station_keys = {
    station: 'station_name', 
    eva: 'eva_number'
};
const stop_keys = {
    eva: 'eva', 
    id: 'uid'
};
const arrival_keys = {
    cde: 'cde', 
    clt: 'clt', 
    cp: 'cp', 
    cpth: 'cpth', 
    cs: 'cs', 
    ct: 'ct', 
    dc: 'dc', 
    fb: 'fb', 
    hi: 'hi', 
    l: 'l', 
    pde: 'pde', 
    pp: 'pp', 
    ppth: 'ppth', 
    ps: 'ps', 
    pt: 'pt', 
    tra: 'tra', 
    wings: 'wings'
};
const triplabel_keys = {
    c: 'c', 
    f: 'f', 
    n: 'n', 
    o: 'o', 
    t: 't'
};
const subtable_keys = {
    timetable: ['m', 's'], 
    s: ['ar', 'tl', 'dp'],
    ar: ['m'],
    dp: ['m'],
    m: ['tl']
};
const table_unique = {
    timetable: [['station'], 'station_name'],
    s: [['uid', 't', 'n'], 'uid, t, n'],
    m: [['id'], 'uid']
}
const table_dicts = {
    timetable: station_keys, 
    s: stop_keys, 
    ar: arrival_keys,
    dp: arrival_keys,
    tl: triplabel_keys
};
const table_names = {
    timetable: 'stations', 
    s: 'stops', 
    ar: 'arrivals',
    dp: 'arrivals',
    m: 'messages',
    tl: 'triplabels'
};

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

    async insert_data(table_key, data, parent, ref_id) {
        try{
            if (table_key == 's') {
                const parts = data['id'].split('-');
                const l = parts.length;

                data['n'] = parts[l - 1]
                data['t'] = parts[l - 2]
                data['uid'] = (l == 4 ? "-" + parts[l - 3] : parts[l - 3]);
                console.log(data)
            }

            const keys = table_dicts[table_key];
            console.log(table_key, parent, ref_id);
            const subset = Object.entries(keys).filter(el => Object.hasOwn(data, el[0]))

            const keyslist = subset.map(el => el[1]);
            const valueslist = subset.map(el => data[el[0]]);

            if (table_key == 's') {
                // keyslist.push()
            }

            var keys_string = `${keyslist.join(', ')}`;
            var values_string = `'${valueslist.join('\', \'')}'`;

            if (table_key == 'ar' || table_key == 'dp') {
                keys_string += `, type`;
                values_string += `, '${table_key}'`;
            }
            if (parent) {
                keys_string += `, ${parent}_id`;
                values_string += `, ${ref_id}`;
            }
            
            console.log(keys_string);
            console.log(values_string);

            const table_name = table_names[table_key];
            const unique_key = table_unique[table_key];
            var row_id = 0;
            if (unique_key) {
                // Insert data (handle conflict on unique element)
                const result = await this.tt_client.query(
                    `INSERT INTO ${table_name} (${keys_string})
                        VALUES(${values_string})
                    ON CONFLICT (${unique_key[1]}) DO NOTHING
                    RETURNING id`
                );
                if (!result.rows[0]) {
                    // break out of loop if stop or message already exists
                    if (table_key == "s" || table_key == "m") {
                        return;
                    } else {
                        const unique_value = `'${unique_key[0].map(el => data[el])}'`;
                        // const unique_value = `'${data[unique_key[0]]}'`;
                        const result2 = await this.tt_client.query(
                            `SELECT id FROM ${table_name} 
                                WHERE ${unique_key[1]}=${unique_value}
                            LIMIT 1`
                        );
                        row_id = result2.rows[0].id;
                    }
                } else {
                    row_id = result.rows[0].id;
                }
            } else {
                // Insert data when no unique key exists
                const result = await this.tt_client.query(
                    `INSERT INTO ${table_name} (${keys_string})
                        VALUES(${values_string})
                    LIMIT 1
                    RETURNING id`
                );
                row_id = result.rows[0].id;
            }

            if (subtable_keys[table_key]) {
                for (const key of subtable_keys[table_key]) {
                    if (data[key] == '' || !data[key]) {
                        continue;
                    }
                    if (Array.isArray(data[key])){
                        for (const d of data[key]) {
                            // console.log("array element");
                            await this.insert_data(key, d, table_names[table_key], row_id);
                        }
                    } else {
                        await this.insert_data(key, data[key], table_names[table_key], row_id);
                    }
                }
            }
        }
        catch (error) {
            throw error;
        }
    }
    
    async store_timetable(tt_data) {
        if (tt_data.timetable == '') {
            return;
        }
        this.insert_data('timetable', tt_data.timetable);
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