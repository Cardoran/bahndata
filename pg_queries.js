const stationData = {
    "number": 8498,
    "ifopt": "de:07131:080058",
    "name": "Heimersheim / Lohrsdorf",
    "mailingAddress": {
      "city": "Bad Neuenahr-Ahrweiler",
      "zipcode": "53474",
      "street": "Greenerweg"
    },
    // ... other fields
  };
  
  async function insertStationData(stationData) {
    const client = await pool.connect();
  
    try {
      await client.query('BEGIN');
  
      // Insert mailing address
      const mailingAddressResult = await client.query(
        `INSERT INTO mailing_addresses (city, zipcode, street)
         VALUES ($1, $2, $3) RETURNING id`,
        [stationData.mailingAddress.city, stationData.mailingAddress.zipcode, stationData.mailingAddress.street]
      );
      const mailingAddressId = mailingAddressResult.rows[0].id;
  
      // Insert regional area
      const regionalAreaResult = await client.query(
        `INSERT INTO regional_areas (number, name, short_name)
         VALUES ($1, $2, $3) RETURNING id`,
        [stationData.regionalbereich.number, stationData.regionalbereich.name, stationData.regionalbereich.shortName]
      );
      const regionalAreaId = regionalAreaResult.rows[0].id;
  
      // Insert task carrier
      const taskCarrierResult = await client.query(
        `INSERT INTO task_carriers (short_name, name)
         VALUES ($1, $2) RETURNING id`,
        [stationData.aufgabentraeger.shortName, stationData.aufgabentraeger.name]
      );
      const taskCarrierId = taskCarrierResult.rows[0].id;
  
      // Insert time table office
      const timeTableOfficeResult = await client.query(
        `INSERT INTO time_table_offices (email, name)
         VALUES ($1, $2) RETURNING id`,
        [stationData.timeTableOffice.email, stationData.timeTableOffice.name]
      );
      const timeTableOfficeId = timeTableOfficeResult.rows[0].id;
  
      // Insert SZentrale
      const szentraleResult = await client.query(
        `INSERT INTO szentrale (number, public_phone_number, name)
         VALUES ($1, $2, $3) RETURNING id`,
        [stationData.szentrale.number, stationData.szentrale.publicPhoneNumber, stationData.szentrale.name]
      );
      const szentraleId = szentraleResult.rows[0].id;
  
      // Insert station management
      const stationManagementResult = await client.query(
        `INSERT INTO station_management (number, name)
         VALUES ($1, $2) RETURNING id`,
        [stationData.stationManagement.number, stationData.stationManagement.name]
      );
      const stationManagementId = stationManagementResult.rows[0].id;
  
      // Insert station
      const stationResult = await client.query(
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
  
      // Insert EVA numbers
      for (const evaNumber of stationData.evaNumbers) {
        await client.query(
          `INSERT INTO eva_numbers (station_id, number, is_main, latitude, longitude)
           VALUES ($1, $2, $3, $4, $5)`,
          [stationId, evaNumber.number, evaNumber.isMain, evaNumber.geographicCoordinates.coordinates[1], evaNumber.geographicCoordinates.coordinates[0]]
        );
      }
  
      // Insert RIL100 identifiers
      for (const ril100 of stationData.ril100Identifiers) {
        await client.query(
          `INSERT INTO ril100_identifiers (
            station_id, ril_identifier, is_main, has_steam_permission, steam_permission,
            latitude, longitude, primary_location_code
          )
          VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
          [
            stationId, ril100.rilIdentifier, ril100.isMain, ril100.hasSteamPermission,
            ril100.steamPermission, ril100.geographicCoordinates.coordinates[1],
            ril100.geographicCoordinates.coordinates[0], ril100.primaryLocationCode
          ]
        );
      }
  
      await client.query('COMMIT');
    } catch (error) {
      await client.query('ROLLBACK');
      console.error('Error inserting data:', error);
    } finally {
      client.release();
    }
  }
  