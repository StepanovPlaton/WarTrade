-- MySQL dump 10.17  Distrib 10.3.22-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: WarTrade
-- ------------------------------------------------------
-- Server version	10.3.22-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Log`
--

DROP TABLE IF EXISTS `Log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` text NOT NULL,
  `type` text NOT NULL,
  `user` text NOT NULL,
  `color` text NOT NULL,
  `text_type` text NOT NULL,
  `look` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Log`
--

LOCK TABLES `Log` WRITE;
/*!40000 ALTER TABLE `Log` DISABLE KEYS */;
INSERT INTO `Log` VALUES (1,'Наступил новый день! Сегодня 20.03.2020','info','system','black','blod','TRUE'),(2,'К игре присоеденился новый игрок - Платон','system','system','blue','normal','TRUE'),(3,'Наступил новый день! Сегодня 21.03.2020','info','system','black','blod','TRUE'),(4,'Наступил новый день! Сегодня 22.03.2020','info','system','black','blod','TRUE'),(5,'Наступил новый день! Сегодня 23.03.2020','info','system','black','blod','TRUE'),(6,'Наступил новый день! Сегодня 24.03.2020','info','system','black','blod','TRUE'),(7,'Наступил новый день! Сегодня 25.03.2020','info','system','black','blod','TRUE'),(8,'Наступил новый день! Сегодня 26.03.2020','info','system','black','blod','TRUE'),(9,'Наступил новый день! Сегодня 27.03.2020','info','system','black','blod','TRUE'),(10,'Наступил новый день! Сегодня 28.03.2020','info','system','black','blod','TRUE'),(11,'Наступил новый день! Сегодня 29.03.2020','info','system','black','blod','TRUE'),(12,'Игрок Платон выложил заявку на 100 монет','game','system','black','normal','TRUE'),(13,'К игре присоеденился новый игрок - Платон2','system','system','blue','normal','TRUE'),(14,'Наступил новый день! Сегодня 30.03.2020','info','system','black','blod','TRUE'),(15,'Игрок Платон2 и игрок Платон заключили сделку на 100 монет','game','system','black','normal','TRUE'),(16,'Наступил новый день! Сегодня 31.03.2020','info','system','black','blod','TRUE'),(17,'Наступил новый день! Сегодня 01.04.2020','info','system','black','blod','TRUE'),(18,'Наступил новый день! Сегодня 02.04.2020','info','system','black','blod','TRUE'),(19,'Наступил новый день! Сегодня 03.04.2020','info','system','black','blod','TRUE'),(20,'Наступил новый день! Сегодня 04.04.2020','info','system','black','blod','TRUE'),(21,'Наступил новый день! Сегодня 05.04.2020','info','system','black','blod','TRUE'),(22,'Наступил новый день! Сегодня 06.04.2020','info','system','black','blod','TRUE'),(23,'Наступил новый день! Сегодня 07.04.2020','info','system','black','blod','TRUE'),(24,'Наступил новый день! Сегодня 08.04.2020','info','system','black','blod','TRUE'),(25,'Наступил новый день! Сегодня 09.04.2020','info','system','black','blod','TRUE'),(26,'Наступил новый день! Сегодня 10.04.2020','info','system','black','blod','TRUE'),(27,'Наступил новый день! Сегодня 11.04.2020','info','system','black','blod','TRUE'),(28,'Наступил новый день! Сегодня 12.04.2020','info','system','black','blod','TRUE'),(29,'Наступил новый день! Сегодня 13.04.2020','info','system','black','blod','TRUE'),(30,'Наступил новый день! Сегодня 14.04.2020','info','system','black','blod','TRUE'),(31,'Наступил новый день! Сегодня 15.04.2020','info','system','black','blod','TRUE'),(32,'Наступил новый день! Сегодня 16.04.2020','info','system','black','blod','TRUE'),(33,'Наступил новый день! Сегодня 17.04.2020','info','system','black','blod','TRUE'),(34,'Наступил новый день! Сегодня 18.04.2020','info','system','black','blod','TRUE'),(35,'Наступил новый день! Сегодня 19.04.2020','info','system','black','blod','TRUE'),(36,'Наступил новый день! Сегодня 20.04.2020','info','system','black','blod','TRUE'),(37,'Наступил новый день! Сегодня 21.04.2020','info','system','black','blod','TRUE'),(38,'Наступил новый день! Сегодня 22.04.2020','info','system','black','blod','TRUE'),(39,'Наступил новый день! Сегодня 23.04.2020','info','system','black','blod','TRUE'),(40,'Наступил новый день! Сегодня 24.04.2020','info','system','black','blod','TRUE'),(41,'Наступил новый день! Сегодня 25.04.2020','info','system','black','blod','TRUE'),(42,'Наступил новый день! Сегодня 26.04.2020','info','system','black','blod','TRUE'),(43,'Наступил новый день! Сегодня 27.04.2020','info','system','black','blod','TRUE'),(44,'Наступил новый день! Сегодня 28.04.2020','info','system','black','blod','TRUE'),(45,'Наступил новый день! Сегодня 29.04.2020','info','system','black','blod','TRUE'),(46,'Наступил новый день! Сегодня 30.04.2020','info','system','black','blod','TRUE'),(47,'Наступил новый день! Сегодня 01.05.2020','info','system','black','blod','TRUE'),(48,'Наступил новый день! Сегодня 02.05.2020','info','system','black','blod','TRUE'),(49,'Наступил новый день! Сегодня 03.05.2020','info','system','black','blod','TRUE'),(50,'Наступил новый день! Сегодня 04.05.2020','info','system','black','blod','TRUE'),(51,'Наступил новый день! Сегодня 05.05.2020','info','system','black','blod','TRUE'),(52,'Наступил новый день! Сегодня 06.05.2020','info','system','black','blod','TRUE'),(53,'Наступил новый день! Сегодня 07.05.2020','info','system','black','blod','TRUE'),(54,'Наступил новый день! Сегодня 08.05.2020','info','system','black','blod','TRUE'),(55,'Наступил новый день! Сегодня 09.05.2020','info','system','black','blod','TRUE'),(56,'Наступил новый день! Сегодня 10.05.2020','info','system','black','blod','TRUE'),(57,'Наступил новый день! Сегодня 11.05.2020','info','system','black','blod','TRUE'),(58,'Наступил новый день! Сегодня 12.05.2020','info','system','black','blod','TRUE'),(59,'Наступил новый день! Сегодня 13.05.2020','info','system','black','blod','TRUE'),(60,'Наступил новый день! Сегодня 14.05.2020','info','system','black','blod','TRUE'),(61,'Наступил новый день! Сегодня 15.05.2020','info','system','black','blod','TRUE'),(62,'Наступил новый день! Сегодня 16.05.2020','info','system','black','blod','TRUE'),(63,'Наступил новый день! Сегодня 17.05.2020','info','system','black','blod','TRUE'),(64,'Наступил новый день! Сегодня 18.05.2020','info','system','black','blod','TRUE'),(65,'Наступил новый день! Сегодня 19.05.2020','info','system','black','blod','TRUE'),(66,'Наступил новый день! Сегодня 20.05.2020','info','system','black','blod','TRUE'),(67,'Наступил новый день! Сегодня 21.05.2020','info','system','black','blod','TRUE'),(68,'Наступил новый день! Сегодня 22.05.2020','info','system','black','blod','TRUE'),(69,'Наступил новый день! Сегодня 23.05.2020','info','system','black','blod','TRUE'),(70,'Наступил новый день! Сегодня 24.05.2020','info','system','black','blod','TRUE'),(71,'Наступил новый день! Сегодня 25.05.2020','info','system','black','blod','TRUE'),(72,'Наступил новый день! Сегодня 26.05.2020','info','system','black','blod','TRUE'),(73,'Наступил новый день! Сегодня 27.05.2020','info','system','black','blod','TRUE'),(74,'Наступил новый день! Сегодня 28.05.2020','info','system','black','blod','TRUE'),(75,'Наступил новый день! Сегодня 29.05.2020','info','system','black','blod','TRUE'),(76,'Наступил новый день! Сегодня 30.05.2020','info','system','black','blod','TRUE'),(77,'В игру вошёл Платон2','system','system','green','normal','TRUE');
/*!40000 ALTER TABLE `Log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Players`
--

DROP TABLE IF EXISTS `Players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Players` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `password` text NOT NULL,
  `ip` text NOT NULL,
  `online` text NOT NULL,
  `money` text NOT NULL,
  `gold` text NOT NULL,
  `wood` text NOT NULL,
  `rock` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Players`
--

LOCK TABLES `Players` WRITE;
/*!40000 ALTER TABLE `Players` DISABLE KEYS */;
INSERT INTO `Players` VALUES (1,'Платон','12345','192.168.32.16','Online','635','7','5','5'),(2,'Платон2','123','192.168.32.16','Online','425','9','5','5');
/*!40000 ALTER TABLE `Players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ResourcesTrend`
--

DROP TABLE IF EXISTS `ResourcesTrend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ResourcesTrend` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` text NOT NULL,
  `gold` int(11) NOT NULL,
  `wood` int(11) NOT NULL,
  `rock` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ResourcesTrend`
--

LOCK TABLES `ResourcesTrend` WRITE;
/*!40000 ALTER TABLE `ResourcesTrend` DISABLE KEYS */;
/*!40000 ALTER TABLE `ResourcesTrend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TradeRequestPlayersList`
--

DROP TABLE IF EXISTS `TradeRequestPlayersList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TradeRequestPlayersList` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` text NOT NULL,
  `name` text NOT NULL,
  `type` text NOT NULL,
  `resource` text NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=204 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TradeRequestPlayersList`
--

LOCK TABLES `TradeRequestPlayersList` WRITE;
/*!40000 ALTER TABLE `TradeRequestPlayersList` DISABLE KEYS */;
/*!40000 ALTER TABLE `TradeRequestPlayersList` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-20 10:56:05
