-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: localhost    Database: bitcoin_forum_scraping
-- ------------------------------------------------------
-- Server version	5.7.17-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `bitcoin_forum_scraping`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `bitcoin_forum_scraping` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `bitcoin_forum_scraping`;

--
-- Table structure for table `user_bitcoins`
--

DROP TABLE IF EXISTS `user_bitcoins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_bitcoins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_profile_id` int(11) DEFAULT NULL,
  `bitcoin_address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_profile_id` (`user_profile_id`),
  CONSTRAINT `user_bitcoins_ibfk_1` FOREIGN KEY (`user_profile_id`) REFERENCES `user_profiles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_bitcoins`
--

LOCK TABLES `user_bitcoins` WRITE;
/*!40000 ALTER TABLE `user_bitcoins` DISABLE KEYS */;
INSERT INTO `user_bitcoins` VALUES (13,84,'1J745nG7LGsBrPjqc9UxGM42Poq9GMNPj8'),(14,85,'3QjDFW4B1gXCAFymCmpMma9JonuWVwXEgT'),(15,86,'1EjdmqPuZ8UskHsRA9LNQQMGyN119FQHrC'),(16,87,'1DADerDP2D9bpDmaBoJzaniKTVCTRratft'),(17,88,'1JemzxBUQTudn9GH4r2HUQpiKUu9ZMUN3c'),(18,89,'1132E662LXDvHBdi2HRhXPru2Z4KhVBGRk');
/*!40000 ALTER TABLE `user_bitcoins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_comments`
--

DROP TABLE IF EXISTS `user_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_profile_id` int(11) DEFAULT NULL,
  `bitcoin_address` varchar(50) DEFAULT NULL,
  `comment_url` varchar(50) DEFAULT NULL,
  `comment_text` varchar(10000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_profile_id` (`user_profile_id`),
  CONSTRAINT `user_comments_ibfk_1` FOREIGN KEY (`user_profile_id`) REFERENCES `user_profiles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_comments`
--

LOCK TABLES `user_comments` WRITE;
/*!40000 ALTER TABLE `user_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profiles`
--

DROP TABLE IF EXISTS `user_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `profile_url` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profiles`
--

LOCK TABLES `user_profiles` WRITE;
/*!40000 ALTER TABLE `user_profiles` DISABLE KEYS */;
INSERT INTO `user_profiles` VALUES (84,'shiunsai','https://bitcointalk.org/index.php?action=profile;u=74353'),(85,'DomainMagnate','https://bitcointalk.org/index.php?action=profile;u=689293'),(86,'beerlover','https://bitcointalk.org/index.php?action=profile;u=152752'),(87,'BitcoinSupremo','https://bitcointalk.org/index.php?action=profile;u=754727'),(88,'Jemzx00','https://bitcointalk.org/index.php?action=profile;u=763568'),(89,'zeaderza','https://bitcointalk.org/index.php?action=profile;u=68115');
/*!40000 ALTER TABLE `user_profiles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-08 17:30:02
