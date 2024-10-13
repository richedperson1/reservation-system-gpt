CREATE DATABASE  IF NOT EXISTS `railway_reservation_management_price`;
USE `railway_reservation_management_price`;

CREATE TABLE `trains` (
  `train_id` int NOT NULL AUTO_INCREMENT,
  `train_no` varchar(10) NOT NULL,
  `train_name` varchar(255) NOT NULL,
  `train_type` enum('Passenger','Express','Superfast') NOT NULL,
  `total_seats` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`train_id`)
);

CREATE TABLE `passengers` (
  `passenger_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `age` int NOT NULL,
  `mobile_no` varchar(15) NOT NULL,
  `aadhar_no` varchar(12) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`passenger_id`),
  UNIQUE KEY `aadhar_no` (`aadhar_no`)
) ;

CREATE TABLE `stations` (
  `station_id` int NOT NULL AUTO_INCREMENT,
  `station_code` varchar(10) NOT NULL,
  `station_name` varchar(255) NOT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`station_id`),
  UNIQUE KEY `station_code` (`station_code`)
) ;



CREATE TABLE `classes` (
  `class_id` int NOT NULL AUTO_INCREMENT,
  `class_name` enum('Sleeper','AC','General') NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`class_id`)
) ;
CREATE TABLE `fares` (
  `fare_id` int NOT NULL AUTO_INCREMENT,
  `train_id` int NOT NULL,
  `class_id` int NOT NULL,
  `start_station_id` int NOT NULL,
  `end_station_id` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`fare_id`),
  KEY `train_id` (`train_id`),
  KEY `class_id` (`class_id`),
  KEY `start_station_id` (`start_station_id`),
  KEY `end_station_id` (`end_station_id`),
  CONSTRAINT `fares_ibfk_1` FOREIGN KEY (`train_id`) REFERENCES `trains` (`train_id`) ON DELETE CASCADE,
  CONSTRAINT `fares_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`)ON DELETE CASCADE,
  CONSTRAINT `fares_ibfk_3` FOREIGN KEY (`start_station_id`) REFERENCES `stations` (`station_id`) ON DELETE CASCADE,
  CONSTRAINT `fares_ibfk_4` FOREIGN KEY (`end_station_id`) REFERENCES `stations` (`station_id`) ON DELETE CASCADE
) ;




-- 1403028831
CREATE TABLE `reservations` (
  `reservation_id` int NOT NULL AUTO_INCREMENT,
  `passenger_id` int NOT NULL,
  `train_id` int NOT NULL,
  `class_id` int NOT NULL,
  `reservation_no` varchar(20) NOT NULL,
  `train_start_station_id` int NOT NULL,
  `destination_station_id` int NOT NULL,
  `reservation_date` date NOT NULL,
  `journey_date` date NOT NULL,
  `fare_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`reservation_id`),
  UNIQUE KEY `reservation_no` (`reservation_no`),
  KEY `passenger_id` (`passenger_id`),
  KEY `train_id` (`train_id`),
  KEY `class_id` (`class_id`),
  KEY `train_start_station_id` (`train_start_station_id`),
  KEY `destination_station_id` (`destination_station_id`),
  KEY `fare_id` (`fare_id`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`passenger_id`) REFERENCES `passengers` (`passenger_id`) ON DELETE CASCADE,
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`train_id`) REFERENCES `trains` (`train_id`) ON DELETE CASCADE,
  CONSTRAINT `reservations_ibfk_3` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`) ON DELETE CASCADE,
  CONSTRAINT `reservations_ibfk_4` FOREIGN KEY (`train_start_station_id`) REFERENCES `stations` (`station_id`)ON DELETE CASCADE,
  CONSTRAINT `reservations_ibfk_5` FOREIGN KEY (`destination_station_id`) REFERENCES `stations` (`station_id`) ON DELETE CASCADE,
  CONSTRAINT `reservations_ibfk_6` FOREIGN KEY (`fare_id`) REFERENCES `fares` (`fare_id`) ON DELETE CASCADE
) ;

CREATE TABLE `routes` (
  `route_id` int NOT NULL AUTO_INCREMENT,
  `train_id` int NOT NULL,
  `station_id` int NOT NULL,
  `arrival_time` time DEFAULT NULL,
  `departure_time` time DEFAULT NULL,
  `sequence` int NOT NULL,
  PRIMARY KEY (`route_id`),
  KEY `train_id` (`train_id`),
  KEY `station_id` (`station_id`),
  CONSTRAINT `routes_ibfk_1` FOREIGN KEY (`train_id`) REFERENCES `trains` (`train_id`) ON DELETE CASCADE,
  CONSTRAINT `routes_ibfk_2` FOREIGN KEY (`station_id`) REFERENCES `stations` (`station_id`) ON DELETE CASCADE
) ;

CREATE TABLE `seats` (
  `seat_id` int NOT NULL AUTO_INCREMENT,
  `train_id` int NOT NULL,
  `seat_no` varchar(10) NOT NULL,
  `class_id` int NOT NULL,
  `availability_status` enum('Booked','Available') DEFAULT 'Available',
  `reservation_id` int DEFAULT NULL,
  PRIMARY KEY (`seat_id`),
  KEY `train_id` (`train_id`),
  KEY `class_id` (`class_id`),
  KEY `reservation_id` (`reservation_id`),
  CONSTRAINT `seats_ibfk_1` FOREIGN KEY (`train_id`) REFERENCES `trains` (`train_id`) ON DELETE CASCADE,
  CONSTRAINT `seats_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`),
  CONSTRAINT `seats_ibfk_3` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`reservation_id`) ON DELETE SET NULL
) ;