drop table triplabels;
drop table messages;
drop table arrivals;
drop table stops;
drop table stations;

CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    eva_number BIGINT,
    station_name VARCHAR(255) NOT NULL,
	CONSTRAINT stations_name_unique UNIQUE ("station_name")
);

CREATE TABLE stops (
	id SERIAL PRIMARY KEY,
	eva integer,
	uid varchar(50),
	t varchar(10),
	n varchar(3),
	stations_id integer,
	CONSTRAINT stops_station_id_fkey FOREIGN KEY (stations_id)
        REFERENCES public.stations (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
	CONSTRAINT stops_uid_unique UNIQUE ("uid", "t", "n")
);

CREATE TABLE arrivals (
    id SERIAL PRIMARY KEY,
	type varchar(2),
	CONSTRAINT ar_type_enum
		CHECK (type IN ('ar', 'dp')),
	cde varchar(50),
	clt varchar(10),
	cp varchar(10),
	cpth varchar,
	cs varchar(1),
	CONSTRAINT ar_cs_enum
		CHECK (cs IN ('p', 'a', 'c')),
	ct varchar(10),
	dc varchar(20),
	fb varchar(20),
	hi varchar(1),
	l varchar(20),
	pde varchar(50),
	pp varchar(10),
	ppth varchar,
	ps varchar(1),
	CONSTRAINT ar_ps_enum
		CHECK (ps IN ('p', 'a', 'c')),
	pt  varchar(10),
	tra  varchar(50),
	wings  varchar,
	stops_id integer,
	CONSTRAINT arrivals_stop_id_fkey FOREIGN KEY (stops_id)
        REFERENCES public.stops (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE messages (
	id SERIAL PRIMARY KEY,
	c integer,
	cat varchar(20),
	del integer,
	dm_int varchar,
	dm_n varchar(20),
	dm_t varchar(1),
	CONSTRAINT m_dm_t_enum
		CHECK (dm_t IN ('s', 'r', 'f', 'x')),
	dm_ts varchar(10),
	ec varchar(10),
	elnk varchar,
	ext varchar,
	valid_from varchar(10),
	uid varchar(50) NOT NULL,
	int varchar,
	o varchar(20),
	pr varchar(1),
	CONSTRAINT m_pr_enum
		CHECK (pr IN ('1', '2', '3', '4')),
	t varchar(1) NOT NULL,
	CONSTRAINT m_t_enum
		CHECK (t IN ('h', 'q', 'f', 'd', 'i', 'u', 'r', 'c')),
	valid_to varchar(10),
	ts varchar(10) NOT NULL,
	stations_id integer,
	CONSTRAINT message_station_id_fkey FOREIGN KEY (stations_id)
        REFERENCES public.stations (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
	stops_id integer,
	CONSTRAINT message_stop_id_fkey FOREIGN KEY (stops_id)
        REFERENCES public.stops (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
	arrivals_id integer,
	CONSTRAINT message_arrival_id_fkey FOREIGN KEY (arrivals_id)
        REFERENCES public.arrivals (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
	CONSTRAINT messages_uid_unique UNIQUE ("uid")
);

CREATE TABLE triplabels (
	id SERIAL PRIMARY KEY,
	c varchar NOT NULL,
	f varchar,
	n varchar NOT NULL,
	o varchar NOT NULL,
	t varchar(1),
	CONSTRAINT tl_t_enum
		CHECK (t IN ('p', 'e', 'z', 's', 'h', 'n')),
	messages_id integer,
	CONSTRAINT triplabel_message_id_fkey FOREIGN KEY (messages_id)
        REFERENCES public.messages (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
	stops_id integer,
	CONSTRAINT triplabel_stop_id_fkey FOREIGN KEY (stops_id)
        REFERENCES public.stops (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);