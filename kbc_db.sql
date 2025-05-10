CREATE DATABASE  IF NOT EXISTS `questions` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `questions`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: questions
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `gamesession`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `gamesession` (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_name` text NOT NULL,
  `difficulty` text NOT NULL,
  `score` int DEFAULT '0',
  `start_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gamesession`
--

LOCK TABLES `gamesession` WRITE;
/*!40000 ALTER TABLE `gamesession` DISABLE KEYS */;
INSERT INTO `gamesession` VALUES (1,'s','Easy',0,'2025-05-09 12:15:50'),(2,'Satabdi','Medium',10,'2025-05-09 12:27:05'),(3,'x','Hard',0,'2025-05-09 12:28:05'),(4,'a','Easy',0,'2025-05-09 12:33:50'),(5,'a','Hard',0,'2025-05-09 12:36:17'),(6,'s','Easy',10,'2025-05-09 12:38:15'),(7,'q','Easy',10,'2025-05-10 10:16:22'),(8,'a','Easy',0,'2025-05-10 10:16:41'),(9,'q','Easy',50,'2025-05-10 10:19:17'),(10,'q','Easy',50,'2025-05-10 10:19:18'),(11,'q','Easy',50,'2025-05-10 10:19:19'),(12,'q','Easy',50,'2025-05-10 10:19:20'),(13,'q','Easy',50,'2025-05-10 10:19:21'),(14,'q','Easy',50,'2025-05-10 10:19:22'),(15,'w','Easy',10,'2025-05-10 10:24:17'),(16,'w','Easy',10,'2025-05-10 10:24:19'),(17,'q','Easy',20,'2025-05-10 10:24:52'),(18,'q','Easy',20,'2025-05-10 10:24:53'),(19,'q','Easy',20,'2025-05-10 10:24:54'),(20,'w','Easy',30,'2025-05-10 10:28:47'),(21,'e','Hard',0,'2025-05-10 10:32:42'),(22,'e','Easy',40,'2025-05-10 10:33:16'),(23,'w','Easy',40,'2025-05-10 10:42:56');
/*!40000 ALTER TABLE `gamesession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE IF NOT EXISTS `quiz` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question` text,
  `optionA` varchar(255) DEFAULT NULL,
  `optionB` varchar(255) DEFAULT NULL,
  `optionC` varchar(255) DEFAULT NULL,
  `optionD` varchar(255) DEFAULT NULL,
  `correctOption` varchar(255) DEFAULT NULL,
  `difficulty` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz`
--

LOCK TABLES `quiz` WRITE;
/*!40000 ALTER TABLE `quiz` DISABLE KEYS */;
INSERT INTO `quiz` VALUES (1,'What is the capital of France?','Paris','Berlin','Rome','Madrid','Paris','Easy'),(2,'Which planet is known as the Red Planet?','Mars','Earth','Venus','Jupiter','Mars','Easy'),(3,'What is the boiling point of water?','90°C','100°C','80°C','120°C','100°C','Easy'),(4,'Who developed the theory of relativity?','Newton','Tesla','Einstein','Darwin','Einstein','Medium'),(5,'What is the square root of 256?','14','16','18','20','16','Medium'),(6,'What is the capital of Australia?','Sydney','Melbourne','Canberra','Perth','Canberra','Hard'),(7,'What is the hardest natural substance?','Gold','Diamond','Platinum','Iron','Diamond','Hard'),(8,'What is the capital of France?','Paris','Berlin','Rome','Madrid','Paris','Easy'),(9,'Which planet is known as the Red Planet?','Mars','Earth','Venus','Jupiter','Mars','Easy'),(10,'What is the boiling point of water?','90°C','100°C','80°C','120°C','100°C','Easy'),(11,'Who developed the theory of relativity?','Newton','Tesla','Einstein','Darwin','Einstein','Medium'),(12,'What is the square root of 256?','14','16','18','20','16','Medium'),(13,'What is the capital of Australia?','Sydney','Melbourne','Canberra','Perth','Canberra','Hard'),(14,'What is the hardest natural substance?','Gold','Diamond','Platinum','Iron','Diamond','Hard'),(15,'What is the capital of France?','Paris','Berlin','Rome','Madrid','Paris','Easy'),(16,'Which planet is known as the Red Planet?','Mars','Earth','Venus','Jupiter','Mars','Easy'),(17,'What is the boiling point of water?','90°C','100°C','80°C','120°C','100°C','Easy'),(18,'Who developed the theory of relativity?','Newton','Tesla','Einstein','Darwin','Einstein','Medium'),(19,'What is the square root of 256?','14','16','18','20','16','Medium'),(20,'What is the capital of Australia?','Sydney','Melbourne','Canberra','Perth','Canberra','Hard'),(21,'What is the hardest natural substance?','Gold','Diamond','Platinum','Iron','Diamond','Hard'),(22,'What is the capital of France?','Paris','Berlin','Rome','Madrid','Paris','Easy'),(23,'Which planet is known as the Red Planet?','Mars','Earth','Venus','Jupiter','Mars','Easy'),(24,'What is the boiling point of water?','90°C','100°C','80°C','120°C','100°C','Easy'),(25,'Who developed the theory of relativity?','Newton','Tesla','Einstein','Darwin','Einstein','Medium'),(26,'What is the square root of 256?','14','16','18','20','16','Medium'),(27,'What is the capital of Australia?','Sydney','Melbourne','Canberra','Perth','Canberra','Hard'),(28,'What is the hardest natural substance?','Gold','Diamond','Platinum','Iron','Diamond','Hard'),(29,'What is the largest mammal in the world?','African Elephant','Blue Whale','Giraffe','Hippopotamus','Blue Whale','Medium'),(30,'Which element has the chemical symbol \'O\'?','Gold','Oxygen',' Osmium','Oganesson','Oxygen','Easy'),(31,'What is the process by which plants make their food?','Respiration','Digestion','Photosynthesis','Transpiration','Photosynthesis','Easy');
/*!40000 ALTER TABLE `quiz` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-10 11:00:09
