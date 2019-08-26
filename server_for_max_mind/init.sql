CREATE DATABASE IF NOT EXISTS mysql_for_server;
USE mysql_for_server;
CREATE TABLE IF NOT EXISTS `collected_data` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`uuid` TEXT,
	`date` DATETIME,
	`remote_ip` TEXT,
	`user_agent` TEXT,
	`accept` TEXT,
	`accept_encoding` TEXT,
	`accept_language` TEXT,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB;
