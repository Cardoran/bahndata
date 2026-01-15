-- Mailing addresses table
CREATE TABLE mailing_addresses (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    zipcode VARCHAR(20),
    street VARCHAR(255)
);

-- Regional areas table
CREATE TABLE regional_areas (
    id SERIAL PRIMARY KEY,
    number INTEGER,
    name VARCHAR(100),
    short_name VARCHAR(50)
);

-- Task carriers table
CREATE TABLE task_carriers (
    id SERIAL PRIMARY KEY,
    short_name VARCHAR(100),
    name VARCHAR(255)
);

-- Time table offices table
CREATE TABLE time_table_offices (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(255)
);

-- SZentrale table
CREATE TABLE szentrale (
    id SERIAL PRIMARY KEY,
    number INTEGER,
    public_phone_number VARCHAR(50),
    name VARCHAR(255)
);

-- Station management table
CREATE TABLE station_management (
    id SERIAL PRIMARY KEY,
    number INTEGER,
    name VARCHAR(255)
);

-- Main stations table
CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    number INTEGER UNIQUE,
    ifopt VARCHAR(50),
    name VARCHAR(255),
    category INTEGER,
    price_category INTEGER,
    has_parking BOOLEAN,
    has_bicycle_parking BOOLEAN,
    has_local_public_transport BOOLEAN,
    has_public_facilities BOOLEAN,
    has_locker_system BOOLEAN,
    has_taxi_rank BOOLEAN,
    has_travel_necessities BOOLEAN,
    has_stepless_access VARCHAR(20),
    has_mobility_service VARCHAR(20),
    has_wifi BOOLEAN,
    has_travel_center BOOLEAN,
    has_railway_mission BOOLEAN,
    has_db_lounge BOOLEAN,
    has_lost_and_found BOOLEAN,
    has_car_rental BOOLEAN,
    federal_state VARCHAR(100),
    federal_state_code VARCHAR(10),
    country_code VARCHAR(10),
    municipality_code VARCHAR(20),
    mailing_address_id INTEGER REFERENCES mailing_addresses(id),
    regional_area_id INTEGER REFERENCES regional_areas(id),
    task_carrier_id INTEGER REFERENCES task_carriers(id),
    time_table_office_id INTEGER REFERENCES time_table_offices(id),
    szentrale_id INTEGER REFERENCES szentrale(id),
    station_management_id INTEGER REFERENCES station_management(id)
);

-- EVA numbers table
CREATE TABLE eva_numbers (
    id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES stations(id),
    number INTEGER,
    is_main BOOLEAN,
    latitude FLOAT,
    longitude FLOAT
);

-- RIL100 identifiers table
CREATE TABLE ril100_identifiers (
    id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES stations(id),
    ril_identifier VARCHAR(20),
    is_main BOOLEAN,
    has_steam_permission BOOLEAN,
    steam_permission VARCHAR(20),
    latitude FLOAT,
    longitude FLOAT,
    primary_location_code VARCHAR(20)
);