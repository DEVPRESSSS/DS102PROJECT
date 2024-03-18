-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 18, 2024 at 01:37 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hardware_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `CategoryID` int(11) NOT NULL,
  `CategoryName` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`CategoryID`, `CategoryName`) VALUES
(3, 'Electrical'),
(2, 'Hardware'),
(1, 'Lumber'),
(5, 'Paint'),
(4, 'Plumbing');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `ProductID` int(11) NOT NULL,
  `ProductName` varchar(255) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `Category` varchar(100) DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `QuantityOnHand` int(11) DEFAULT NULL,
  `CategoryID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`ProductID`, `ProductName`, `Description`, `Category`, `Price`, `QuantityOnHand`, `CategoryID`) VALUES
(1, '2x4 Stud', 'Standard framing lumber, 8 feet long', 'Lumber', 5.99, 100, 1),
(2, 'Plywood Sheathing', 'Structural plywood, 4 feet by 8 feet', NULL, 24.99, 50, 1),
(3, 'Drywall Sheet', 'Standard drywall, 4 feet by 8 feet', NULL, 12.99, 75, 1),
(4, 'Nails', 'Common nails, 3 inches, box of 50', NULL, 9.99, 200, 2),
(5, 'Screws', 'Drywall screws, 1-1/4 inches, box of 100', NULL, 7.99, 150, 2),
(6, 'Electrical Wire', '14-gauge electrical wire, 100 feet', NULL, 39.99, 30, 3),
(7, 'Electrical Outlets', 'Standard electrical outlets, pack of 10', NULL, 12.99, 20, 3),
(8, 'PVC Pipe', 'Schedule 40 PVC pipe, 1 inch diameter, 10 feet', NULL, 4.99, 50, 4),
(9, 'Sink Faucet', 'Standard kitchen sink faucet', NULL, 49.99, 15, 4),
(10, 'Interior Paint', 'Latex interior paint, 1 gallon, eggshell finish', 'Plumbing', 29.99, 40, 5),
(11, 'Exterior Paint', 'Acrylic exterior paint, 1 gallon, satin finish', 'Electrical', 39.99, 25, 5),
(13, 'mb', 'walang katulad', 'Lumber', 99999999.99, 1, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `sellers_tbl`
--

CREATE TABLE `sellers_tbl` (
  `seller_id` int(11) NOT NULL,
  `fullname` varchar(200) NOT NULL,
  `contact` int(11) NOT NULL,
  `address` varchar(150) NOT NULL,
  `email` varchar(60) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sellers_tbl`
--

INSERT INTO `sellers_tbl` (`seller_id`, `fullname`, `contact`, `address`, `email`, `password`) VALUES
(33, 'ddadada', 1212121, 'erdgdg', 'admin', '123'),
(34, 'fsfsf', 0, 'sfsf', 'fsfs', 'fsfs');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`CategoryID`),
  ADD UNIQUE KEY `CategoryName` (`CategoryName`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`ProductID`),
  ADD KEY `fk_category` (`CategoryID`);

--
-- Indexes for table `sellers_tbl`
--
ALTER TABLE `sellers_tbl`
  ADD PRIMARY KEY (`seller_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `CategoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `sellers_tbl`
--
ALTER TABLE `sellers_tbl`
  MODIFY `seller_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `fk_category` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`CategoryID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
