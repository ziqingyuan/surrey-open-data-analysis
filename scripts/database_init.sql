DROP TABLE IF EXISTS transit_stop;

DROP TABLE IF EXISTS restaurant;

CREATE TABLE transit_stop (
    id INT PRIMARY KEY COMMENT 'The transit stop ID',
    name VARCHAR(255) COMMENT 'The transit stop name',
    lon FLOAT COMMENT 'The transit stop longitude',
    lat FLOAT COMMENT 'The transit stop latitude',
    city VARCHAR(255) COMMENT 'The city of the transit stop',
    utm_x FLOAT COMMENT 'The transit stop UTM X coordinate',
    utm_y FLOAT COMMENT 'The transit stop UTM Y coordinate'
);

CREATE TABLE restaurant (
    tracking_number VARCHAR(255) PRIMARY KEY COMMENT 'The restaurant tracking number',
    lon FLOAT COMMENT 'The restaurant longitude',
    lat FLOAT COMMENT 'The restaurant latitude',
    name VARCHAR(255) COMMENT 'The restaurant name',
    city VARCHAR(255) COMMENT 'The restaurant city',
    address VARCHAR(255) COMMENT 'The restaurant address',
    utm_x FLOAT COMMENT 'The restaurant UTM X coordinate',
    utm_y FLOAT COMMENT 'The restaurant UTM Y coordinate'
);
