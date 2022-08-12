-- First, clear up tables to create new ones 
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS transactions;


-- Create reservations table with data for reservations
CREATE TABLE reservations (
	reservation_id integer NOT NULL,
	facility character varying(40) NOT NULL,
	recurring_number integer NOT NULL,
	reservation_date DATE NOT NULL,
	resource character varying(40) NOT NULL,
	client_id character varying(40) NOT NULL,
	start_time REAL NOT NULL,
	end_time  REAL NOT NULL,
	status character varying(3) NOT NULL,
	primary key (reservation_id, recurring_number)
	);


-- Create users table with data for users
-- FIXME
CREATE TABLE users (
	user_id character varying(40) NOT NULL,
	role character varying(40) NOT NULL,
	balance integer DEFAULT 0,
	active character varying(40) DEFAULT 'yes' NOT NULL, 
	salt character varying(40) NOT NULL,
	hash character varying(40) NOT NULL,
	primary key (user_id)
	);


-- Create reservations table with data for reservations
CREATE TABLE transactions (
	transaction_id character varying(40) NOT NULL,
	transaction_type character varying(40) NOT NULL,
	transaction_amount integer NOT NULL,
	transaction_timestamp DATETIME NOT NULL,
	user_id character varying(40) NOT NULL,
	reservation_id integer NOT NULL,
	primary key (transaction_id),
	foreign key (user_id) references users ON UPDATE CASCADE ON DELETE CASCADE,
	foreign key (reservation_id) references reservations ON UPDATE CASCADE ON DELETE CASCADE
	);