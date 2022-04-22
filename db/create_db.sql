CREATE TABLE jobs(
    identifier varchar(10) primary key,
	status int,
	username varchar(20),
	create_time DATETIME,
	last_update DATETIME);

CREATE TABLE uploads(
    identifier varchar(30) primary key,
	data_type vharchar(20),
	username varchar(20),
	create_time DATETIME,
	last_update DATETIME);

CREATE TRIGGER insert_create_time_Trigger
AFTER INSERT ON jobs
BEGIN
    UPDATE jobs SET create_time = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'), last_update = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW') WHERE identifier = NEW.identifier;
END;

CREATE TRIGGER update_last_update_Trigger
AFTER UPDATE ON jobs
BEGIN
    UPDATE jobs SET last_update = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW') WHERE identifier = NEW.identifier;
END;

CREATE TRIGGER insert_upload_create_time_Trigger
AFTER INSERT ON uploads
BEGIN
    UPDATE uplads SET create_time = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'), last_update = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW') WHERE identifier = NEW.identifier;
END;

CREATE TRIGGER update_upload_last_update_Trigger
AFTER UPDATE ON uploads
BEGIN
    UPDATE uploads SET last_update = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW') WHERE identifier = NEW.identifier;
END;
