-- DROP TABLE IF EXISTS donor;
-- DROP TABLE IF EXISTS blood;
-- DROP TABLE IF EXISTS hospital;
-- DROP TABLE IF EXISTS requests;

CREATE TABLE IF NOT EXISTS donor(
	donor_id VARCHAR(6) UNIQUE,
	donor_name VARCHAR(50) NOT NULL,
	donor_contact VARCHAR(11) NOT NULL,
	donor_address VARCHAR(100) NOT NULL,
	PRIMARY KEY (donor_id)
	);

CREATE TABLE IF NOT EXISTS blood(
	blood_id VARCHAR(7) UNIQUE,
	blood_type VARCHAR(15) NOT NULL,
	date_donated DATE NOT NULL,
	donor_id VARCHAR(6) NOT NULL,
	PRIMARY KEY (blood_id),
	FOREIGN KEY (donor_id) REFERENCES donor(donor_id)
		ON DELETE CASCADE
	);

CREATE TABLE IF NOT EXISTS hospital(
	hosp_name_abbrev VARCHAR(10) UNIQUE,
	hosp_name VARCHAR(100) NOT NULL,
	hosp_address VARCHAR(100) NOT NULL,
	hosp_telephone VARCHAR(8) NOT NULL,
	PRIMARY KEY (hosp_name_abbrev)
	);

CREATE TABLE IF NOT EXISTS blood_request(
	blood_id VARCHAR(7) NOT NULL,
	hosp_name_abbrev VARCHAR(10) NOT NULL,
	blood_type VARCHAR(15) NOT NULL,
	bags INTEGER NOT NULL,
	date_requested DATE NOT NULL,
	physician VARCHAR(50) NOT NULL,
	PRIMARY KEY (blood_id, hosp_name_abbrev),
	FOREIGN KEY (blood_id) REFERENCES blood(blood_id)
		ON DELETE CASCADE,
	FOREIGN KEY (hosp_name_abbrev) REFERENCES hospital(hosp_name_abbrev)
		ON DELETE CASCADE
		ON UPDATE CASCADE
	);
