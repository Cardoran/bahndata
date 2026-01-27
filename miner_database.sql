CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    eva_number BIGINT NOT NULL,
    station_name VARCHAR(255) NOT NULL
);

CREATE TABLE messages (
	key SERIAL PRIMARY KEY,
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
	from varchar(10),
	id varchar(50) NOT NULL,
	int varchar,
	o varchar(20),
	pr varchar(1),
	CONSTRAINT m_pr_enum
		CHECK (pr IN ('1', '2', '3', '4')),
	t varchar(1) NOT NULL,
	CONSTRAINT m_t_enum
		CHECK (pr IN ('h', 'q', 'f', 'd', 'i', 'u', 'r', 'c')),
	tl_c varchar(20),--required
	tl_f varchar(10),
	tl_n varchar(20),--required
	tl_o varchar(10),--required
	tl_t varchar(1),
	CONSTRAINT m_tl_t_enum
		CHECK (pr IN ('p', 'e', 'z', 's', 'h', 'n')),
	to varchar(10),
	ts varchar(10) NOT NULL
);

CREATE TABLE stops (
	ar_cde 
	ar_clt 
	ar_cp 
	ar_cpth 
	ar_cs 
	ar_ct 
	ar_dc 
	ar_fb 
	ar_hi 
	ar_l 
	ar_m
);