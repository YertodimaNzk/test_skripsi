CREATE DATABASE  IF NOT EXISTS `pharmadia` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `pharmadia`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: pharmadia
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.24-MariaDB

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
-- Table structure for table `aboutus`
--

DROP TABLE IF EXISTS `about_us`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `about_us` (
  `nama` varchar(200) NOT NULL,
  `Deskripsi` varchar(500) NOT NULL,
  `sosial_media` varchar(200) NOT NULL,
  `nomor_telepon` varchar(200) NOT NULL,
  `auth_id` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `created_by` varchar(200) NOT NULL,
  `updated_by` varchar(200) NOT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`auth_id`),
  CONSTRAINT `fk_aboutus_authorization1` FOREIGN KEY (`auth_id`) REFERENCES `authorization` (`auth_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aboutus`
--

LOCK TABLES `about_us` WRITE;
/*!40000 ALTER TABLE `aboutus` DISABLE KEYS */;
/*!40000 ALTER TABLE `aboutus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authorization`
--

DROP TABLE IF EXISTS `authorization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authorization` (
  `auth_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  PRIMARY KEY (`auth_id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authorization`
--

LOCK TABLES `authorization` WRITE;
/*!40000 ALTER TABLE `authorization` DISABLE KEYS */;
INSERT INTO `authorization` VALUES (1,'Alexander','admin123');
/*!40000 ALTER TABLE `authorization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keyword`
--

DROP TABLE IF EXISTS `keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keyword` (
  `keyword_id` int(11) NOT NULL AUTO_INCREMENT,
  `penyakit_id` int(11) NOT NULL,
  `auth_id` int(11) NOT NULL,
  `keyword_nama` varchar(200) NOT NULL UNIQUE,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by` varchar(200) NOT NULL,
  `updated_by` varchar(200) NOT NULL,
  PRIMARY KEY (`keyword_id`,`penyakit_id`,`auth_id`),
  CONSTRAINT `fk_keyword_penyakit1` FOREIGN KEY (`penyakit_id`, `auth_id`) REFERENCES `penyakit` (`penyakit_id`, `auth_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keyword`
--

LOCK TABLES `keyword` WRITE;
/*!40000 ALTER TABLE `keyword` DISABLE KEYS */;
/*!40000 ALTER TABLE `keyword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keywordbank`
--

DROP TABLE IF EXISTS `keywordbank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keywordbank` (
  `keywordbank_id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword_nama` varchar(200) NOT NULL,
  `keyword_id` int(11) NOT NULL,
  `auth_id` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`keywordbank_id`,`keyword_id`,`auth_id`),
  KEY `fk_keywordbank_authorization1_idx` (`auth_id`),
  KEY `fk_keywordbank_keyword1` (`keyword_id`),
  CONSTRAINT `fk_keywordbank_authorization1` FOREIGN KEY (`auth_id`) REFERENCES `authorization` (`auth_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_keywordbank_keyword1` FOREIGN KEY (`keyword_id`) REFERENCES `keyword` (`keyword_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keywordbank`
--

LOCK TABLES `keywordbank` WRITE;
/*!40000 ALTER TABLE `keywordbank` DISABLE KEYS */;
/*!40000 ALTER TABLE `keywordbank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `masukan`
--

DROP TABLE IF EXISTS `masukan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `masukan` (
  `masukan_id` int(11) NOT NULL AUTO_INCREMENT,
  `masukan` varchar(1000) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`masukan_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `masukan`
--

LOCK TABLES `masukan` WRITE;
/*!40000 ALTER TABLE `masukan` DISABLE KEYS */;
/*!40000 ALTER TABLE `masukan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `penyakit`
--

DROP TABLE IF EXISTS `penyakit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `penyakit` (
  `penyakit_id` int(11) NOT NULL AUTO_INCREMENT,
  `auth_id` int(11) NOT NULL,
  `penyakit_nama` varchar(200) NOT NULL,
  `penyakit_penanganan` varchar(200) NOT NULL,
  `penyakit_obat` varchar(200) NOT NULL,
  `penyakit_deskripsi` varchar(5000) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by` varchar(200) NOT NULL,
  `update_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `update_by` varchar(200) NOT NULL,
  PRIMARY KEY (`penyakit_id`,`auth_id`),
  KEY `fk_penyakit_authorization_idx` (`auth_id`),
  CONSTRAINT `fk_penyakit_authorization` FOREIGN KEY (`auth_id`) REFERENCES `authorization` (`auth_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `penyakit`
--

LOCK TABLES `penyakit` WRITE;
/*!40000 ALTER TABLE `penyakit` DISABLE KEYS */;
INSERT INTO `penyakit` VALUES (3,1,'Batuk','Penanganan pertama untuk batuk adalah Istirahat, minum banyak cairan, dan penggunaan obat batuk seperti ekspektoran atau antitusif.','Dextromethorphan, Guaifenesin, atau Codeine.','Batuk dapat disebabkan oleh Infeksi virus atau bakteri pada saluran pernapasan, alergi, atau iritasi akibat asap atau polusi udara.','2024-05-29 13:49:42','Alexander','2024-05-29 13:49:42','Alexander'),(4,1,'Demam','Penanganan awal untuk demam adalah minum obat penurun demam seperti Parasetamol atau Ibuprofen, istirahat, dan minum banyak cairan untuk mencegah dehidrasi.','Parasetamol, Ibuprofen, atau Aspirin.','Demam adalah sebuah reaksi tubuh terhadap infeksi virus atau bakteri, inflamasi, atau penyakit lain.','2024-05-29 13:51:20','Alexander','2024-05-29 13:51:20','Alexander'),(5,1,'Diare','Penanganan pertama untuk diare adalah dengan minum banyak cairan untuk mengganti cairan yang hilang, mengonsumsi makanan ringan, dan menghindari makanan yang menyebabkan iritasi seperti pedas dan asam','Loperamide atau Racecadotril.','Diare umumnya disebabkan oleh Infeksi virus, bakteri, atau parasit; konsumsi makanan atau air yang terkontaminasi; atau reaksi terhadap obat-obatan.','2024-05-29 13:53:29','Alexander','2024-05-29 13:53:29','Alexander'),(6,1,'Asma','Penanganan pertama untuk asma dengan segera jauhi pemicu alergi, gunakan inhaler bronkodilator atau steroid, dan mengatur pola hidup sehat.','Inhaler bronkodilator (Albuterol), inhaler steroid (Flutikason), atau Montelukast ','Asma biasanya disebabkan oleh alergi, iritasi saluran pernapasan,dan gangguan pernapasan kronis yang menyebabkan penyempitan saluran udara.','2024-05-29 13:55:44','Alexander','2024-05-29 13:55:44','Alexander');
/*!40000 ALTER TABLE `penyakit` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-15  0:39:33
