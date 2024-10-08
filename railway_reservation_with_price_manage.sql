CREATE DATABASE IF NOT EXISTS `railway_reservation_management_price` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `railway_reservation_management_price`;

-- Passengers Table
DROP TABLE IF EXISTS `passengers`;
CREATE TABLE `passengers` (
  `passenger_id` INT AUTO_INCREMENT PRIMARY KEY,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `gender` ENUM('Male', 'Female', 'Other') NOT NULL,
  `age` INT NOT NULL,
  `mobile_no` VARCHAR(15) NOT NULL,
  `aadhar_no` VARCHAR(12) UNIQUE,
  `email` VARCHAR(255),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Stations Table
DROP TABLE IF EXISTS `stations`;
CREATE TABLE `stations` (
  `station_id` INT AUTO_INCREMENT PRIMARY KEY,
  `station_code` VARCHAR(10) UNIQUE NOT NULL,
  `station_name` VARCHAR(255) NOT NULL,
  `city` VARCHAR(100),
  `state` VARCHAR(100),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Trains Table
DROP TABLE IF EXISTS `trains`;
CREATE TABLE `trains` (
  `train_id` INT AUTO_INCREMENT PRIMARY KEY,
  `train_no` VARCHAR(10) NOT NULL,
  `train_name` VARCHAR(255) NOT NULL,
  `train_type` ENUM('Passenger', 'Express', 'Superfast') NOT NULL,
  `total_seats` INT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Routes Table (To define train routes, start and end stations)
DROP TABLE IF EXISTS `routes`;
CREATE TABLE `routes` (
  `route_id` INT AUTO_INCREMENT PRIMARY KEY,
  `train_id` INT NOT NULL,
  `station_id` INT NOT NULL,
  `arrival_time` TIME,
  `departure_time` TIME,
  `sequence` INT NOT NULL,
  FOREIGN KEY (`train_id`) REFERENCES `trains`(`train_id`) ON DELETE CASCADE,
  FOREIGN KEY (`station_id`) REFERENCES `stations`(`station_id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Classes Table (Ticket classes such as AC, Sleeper, etc.)
DROP TABLE IF EXISTS `classes`;
CREATE TABLE `classes` (
  `class_id` INT AUTO_INCREMENT PRIMARY KEY,
  `class_name` ENUM('Sleeper', 'AC', 'General') NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Fares Table (Pre-set prices for ticket types based on class, route, and distance)
DROP TABLE IF EXISTS `fares`;
CREATE TABLE `fares` (
  `fare_id` INT AUTO_INCREMENT PRIMARY KEY,
  `train_id` INT NOT NULL,
  `class_id` INT NOT NULL,
  `start_station_id` INT NOT NULL,
  `end_station_id` INT NOT NULL,
  `price` DECIMAL(10, 2) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`train_id`) REFERENCES `trains`(`train_id`) ON DELETE CASCADE,
  FOREIGN KEY (`class_id`) REFERENCES `classes`(`class_id`),
  FOREIGN KEY (`start_station_id`) REFERENCES `stations`(`station_id`),
  FOREIGN KEY (`end_station_id`) REFERENCES `stations`(`station_id`)
) ENGINE=InnoDB;

-- Reservations Table
DROP TABLE IF EXISTS `reservations`;
CREATE TABLE `reservations` (
  `reservation_id` INT AUTO_INCREMENT PRIMARY KEY,
  `passenger_id` INT NOT NULL,
  `train_id` INT NOT NULL,
  `class_id` INT NOT NULL,
  `reservation_no` VARCHAR(20) UNIQUE NOT NULL,
  `train_start_station_id` INT NOT NULL,
  `destination_station_id` INT NOT NULL,
  `reservation_date` DATE NOT NULL,
  `journey_date` DATE NOT NULL,
  `fare_id` INT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`passenger_id`) REFERENCES `passengers`(`passenger_id`) ON DELETE CASCADE,
  FOREIGN KEY (`train_id`) REFERENCES `trains`(`train_id`) ON DELETE CASCADE,
  FOREIGN KEY (`class_id`) REFERENCES `classes`(`class_id`),
  FOREIGN KEY (`train_start_station_id`) REFERENCES `stations`(`station_id`),
  FOREIGN KEY (`destination_station_id`) REFERENCES `stations`(`station_id`),
  FOREIGN KEY (`fare_id`) REFERENCES `fares`(`fare_id`)
) ENGINE=InnoDB;

-- Seats Table
DROP TABLE IF EXISTS `seats`;
CREATE TABLE `seats` (
  `seat_id` INT AUTO_INCREMENT PRIMARY KEY,
  `train_id` INT NOT NULL,
  `seat_no` VARCHAR(10) NOT NULL,
  `class_id` INT NOT NULL,
  `availability_status` ENUM('Booked', 'Available') DEFAULT 'Available',
  `reservation_id` INT,
  FOREIGN KEY (`train_id`) REFERENCES `trains`(`train_id`) ON DELETE CASCADE,
  FOREIGN KEY (`class_id`) REFERENCES `classes`(`class_id`),
  FOREIGN KEY (`reservation_id`) REFERENCES `reservations`(`reservation_id`) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Reservation Audit Table (For tracking reservation changes)
DROP TABLE IF EXISTS `reservation_audit`;
CREATE TABLE `reservation_audit` (
  `audit_id` INT AUTO_INCREMENT PRIMARY KEY,
  `reservation_id` INT NOT NULL,
  `status_change` VARCHAR(255),
  `updated_by` VARCHAR(255),
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`reservation_id`) REFERENCES `reservations`(`reservation_id`) ON DELETE CASCADE
) ENGINE=InnoDB;
