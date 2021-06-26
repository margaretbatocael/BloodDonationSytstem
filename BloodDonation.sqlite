-- DROP TABLE IF EXISTS donor;
-- DROP TABLE IF EXISTS blood;
-- DROP TABLE IF EXISTS hospital;
-- DROP TABLE IF EXISTS requests;

CREATE TABLE IF NOT EXISTS donor
(
	donor_id TEXT UNIQUE PRIMARY KEY,
	donor_name TEXT NOT NULL,
	donor_contact TEXT NOT NULL,
	donor_address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS blood
(
	blood_id TEXT UNIQUE PRIMARY KEY,
	blood_type TEXT NOT NULL,
	date_donated DATE NOT NULL,
	donor_id TEXT NOT NULL,
	FOREIGN KEY (donor_id) REFERENCES donor(donor_id)
);

CREATE TABLE IF NOT EXISTS hospital
(
	hosp_name_abbrev TEXT UNIQUE PRIMARY KEY,
	hosp_name TEXT NOT NULL,
	hosp_address TEXT NOT NULL,
	hosp_telephone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS requests
(
	blood_id TEXT NOT NULL,
	hosp_name_abbrev TEXT NOT NULL,
	blood_type TEXT NOT NULL,
	bags INTEGER NOT NULL,
	date_requested DATE NOT NULL,
	physician TEXT NOT NULL,
	PRIMARY KEY (blood_id, hosp_name_abbrev),
	FOREIGN KEY (blood_id) REFERENCES blood(blood_id),
	FOREIGN KEY (hosp_name_abbrev) REFERENCES hospital(hosp_name_abbrev)
);