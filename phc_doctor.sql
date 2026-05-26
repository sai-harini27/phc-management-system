-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 08, 2026 at 11:27 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `phc_doctor`
--

-- --------------------------------------------------------

--
-- Table structure for table `ph_admin`
--

CREATE TABLE `ph_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ph_admin`
--

INSERT INTO `ph_admin` (`username`, `password`, `email`) VALUES
('admin', 'admin', 'bgeduscanner@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `ph_attendance`
--

CREATE TABLE `ph_attendance` (
  `id` int(11) NOT NULL,
  `docid` varchar(20) NOT NULL,
  `phc_id` varchar(20) NOT NULL,
  `geo_image` varchar(30) NOT NULL,
  `latitude` varchar(20) NOT NULL,
  `longitude` varchar(20) NOT NULL,
  `att_date` varchar(20) NOT NULL,
  `att_time` varchar(20) NOT NULL,
  `face_st` int(11) NOT NULL,
  `geo_st` int(11) NOT NULL,
  `time_st` int(11) NOT NULL,
  `att_st` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `count_random` int(11) NOT NULL,
  `count_att_fail` int(11) NOT NULL,
  `count_geo` int(11) NOT NULL,
  `count_geo_fail` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ph_attendance`
--

INSERT INTO `ph_attendance` (`id`, `docid`, `phc_id`, `geo_image`, `latitude`, `longitude`, `att_date`, `att_time`, `face_st`, `geo_st`, `time_st`, `att_st`, `month`, `year`, `count_random`, `count_att_fail`, `count_geo`, `count_geo_fail`) VALUES
(1, 'D1', 'P001', 'D1_1.jpg', '10.815500', '78.696500', '2025-04-01', '06:59:08', 0, 0, 0, 0, 4, 2025, 0, 0, 0, 0),
(2, 'D1', 'P001', 'D1_2.jpg', '10.861600', '78.647000', '2025-04-02', '08:51:54', 1, 1, 1, 0, 4, 2025, 0, 0, 0, 0),
(3, 'D1', 'P001', 'D1_2.jpg', '10.815500', '78.696500', '2025-04-03', '11:18:04', 1, 2, 2, 0, 4, 2025, 0, 0, 0, 0),
(4, 'D1', 'P001', 'D1_2.jpg', '10.815500', '78.696500', '2025-04-04', '11:19:52', 1, 1, 1, 1, 4, 2025, 0, 0, 0, 0),
(5, 'D1', 'P001', 'D1_2.jpg', '10.815500', '78.696500', '2025-04-05', '11:22:07', 1, 1, 1, 1, 4, 2025, 0, 0, 0, 0),
(6, 'D1', 'P001', 'D1_8.jpg', '10.815500', '78.696500', '2025-04-06', '10:05:00', 1, 1, 1, 1, 4, 2025, 0, 0, 0, 0),
(7, 'D2', 'P001', '', '', '', '2025-04-06', '', 0, 0, 0, 0, 4, 2025, 0, 0, 0, 0),
(8, 'D1', 'P001', 'D1_10.jpg', '10.851774', '78.65502', '2025-04-07', '23:27:00', 2, 1, 2, 2, 4, 2025, 0, 0, 0, 0),
(9, 'D2', 'P001', '', '', '', '2025-04-07', '', 0, 0, 0, 0, 4, 2025, 0, 0, 0, 0),
(10, 'D1', 'P001', 'D1_12.jpg', '10.815500', '78.696500', '2025-04-08', '22:13:59', 2, 2, 2, 2, 4, 2025, 0, 0, 0, 0),
(11, 'D2', 'P001', '', '', '', '2025-04-08', '', 0, 0, 0, 0, 4, 2025, 0, 0, 0, 0),
(12, 'D1', 'P001', '', '', '', '2025-04-09', '', 0, 0, 0, 0, 4, 2025, 0, 0, 0, 0),
(13, 'D2', 'P001', '', '', '', '2025-04-09', '', 0, 0, 0, 0, 4, 2025, 0, 0, 0, 0),
(14, 'D1', 'P001', 'D1_16.jpg', '0.000000', '0.000000', '2025-12-17', '18:01:13', 1, 2, 2, 2, 12, 2025, 0, 0, 0, 0),
(15, 'D2', 'P001', '', '', '', '2025-12-17', '', 0, 0, 0, 0, 12, 2025, 0, 0, 0, 0),
(16, 'D1', 'P001', 'D1_18.jpg', '10.836417', '78.689181', '2025-12-18', '17:39:36', 1, 1, 2, 1, 12, 2025, 0, 0, 0, 0),
(17, 'D2', 'P001', '', '', '', '2025-12-18', '', 0, 0, 0, 0, 12, 2025, 0, 0, 0, 0),
(18, 'D1', 'P001', '', '', '', '2025-12-22', '', 0, 0, 0, 0, 12, 2025, 0, 0, 0, 0),
(19, 'D2', 'P001', '', '', '', '2025-12-22', '', 0, 0, 0, 0, 12, 2025, 0, 0, 0, 0),
(20, 'D1', 'P001', '', '', '', '2026-02-02', '', 0, 0, 0, 0, 2, 2026, 0, 0, 0, 0),
(21, 'D2', 'P001', '', '', '', '2026-02-02', '', 0, 0, 0, 0, 2, 2026, 0, 0, 0, 0),
(22, 'D1', 'P001', '', '', '', '2026-02-03', '', 0, 0, 0, 0, 2, 2026, 0, 0, 0, 0),
(23, 'D2', 'P001', '', '', '', '2026-02-03', '', 0, 0, 0, 0, 2, 2026, 0, 0, 0, 0),
(24, 'D1', 'P001', '', '', '', '2026-03-08', '', 0, 0, 0, 0, 3, 2026, 0, 0, 0, 0),
(25, 'D2', 'P001', '', '', '', '2026-03-08', '', 0, 0, 0, 0, 3, 2026, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `ph_ddhs`
--

CREATE TABLE `ph_ddhs` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `district` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ph_ddhs`
--

INSERT INTO `ph_ddhs` (`id`, `name`, `mobile`, `email`, `district`, `uname`, `pass`) VALUES
(1, 'Harish', 9894442716, 'bgeduscanner@gmail.com', 'Salem', 'DH1', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `ph_doctor`
--

CREATE TABLE `ph_doctor` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `district` varchar(30) NOT NULL,
  `specialized` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `fimg` varchar(20) NOT NULL,
  `phc_id` varchar(20) NOT NULL,
  `stime` int(11) NOT NULL,
  `etime` int(11) NOT NULL,
  `smin` int(11) NOT NULL,
  `emin` int(11) NOT NULL,
  `smode` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ph_doctor`
--

INSERT INTO `ph_doctor` (`id`, `name`, `gender`, `mobile`, `email`, `district`, `specialized`, `uname`, `pass`, `fimg`, `phc_id`, `stime`, `etime`, `smin`, `emin`, `smode`) VALUES
(1, 'Dr. P.Raman, MBBS', 'Male', 9874522555, 'raman@gmail.com', 'Salem', 'General Physician', 'D1', '1234', 'User.1.60.jpg', 'P001', 10, 20, 0, 30, 0),
(2, 'Dr. R.Geetha, M.D', 'Female', 8956222541, 'geetha@gmail.com', 'Chennai', 'General Physician', 'D2', '1234', '', 'P001', 9, 17, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `ph_face`
--

CREATE TABLE `ph_face` (
  `id` int(11) NOT NULL,
  `vid` int(11) NOT NULL,
  `vface` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ph_face`
--

INSERT INTO `ph_face` (`id`, `vid`, `vface`) VALUES
(1, 1, 'User.1.2.jpg'),
(2, 1, 'User.1.3.jpg'),
(3, 1, 'User.1.4.jpg'),
(4, 1, 'User.1.5.jpg'),
(5, 1, 'User.1.6.jpg'),
(6, 1, 'User.1.7.jpg'),
(7, 1, 'User.1.8.jpg'),
(8, 1, 'User.1.9.jpg'),
(9, 1, 'User.1.10.jpg'),
(10, 1, 'User.1.11.jpg'),
(11, 1, 'User.1.12.jpg'),
(12, 1, 'User.1.13.jpg'),
(13, 1, 'User.1.14.jpg'),
(14, 1, 'User.1.15.jpg'),
(15, 1, 'User.1.16.jpg'),
(16, 1, 'User.1.17.jpg'),
(17, 1, 'User.1.18.jpg'),
(18, 1, 'User.1.19.jpg'),
(19, 1, 'User.1.20.jpg'),
(20, 1, 'User.1.21.jpg'),
(21, 1, 'User.1.22.jpg'),
(22, 1, 'User.1.23.jpg'),
(23, 1, 'User.1.24.jpg'),
(24, 1, 'User.1.25.jpg'),
(25, 1, 'User.1.26.jpg'),
(26, 1, 'User.1.27.jpg'),
(27, 1, 'User.1.28.jpg'),
(28, 1, 'User.1.29.jpg'),
(29, 1, 'User.1.30.jpg'),
(30, 1, 'User.1.31.jpg'),
(31, 1, 'User.1.32.jpg'),
(32, 1, 'User.1.33.jpg'),
(33, 1, 'User.1.34.jpg'),
(34, 1, 'User.1.35.jpg'),
(35, 1, 'User.1.36.jpg'),
(36, 1, 'User.1.37.jpg'),
(37, 1, 'User.1.38.jpg'),
(38, 1, 'User.1.39.jpg'),
(39, 1, 'User.1.40.jpg'),
(40, 1, 'User.1.41.jpg'),
(41, 1, 'User.1.42.jpg'),
(42, 1, 'User.1.43.jpg'),
(43, 1, 'User.1.44.jpg'),
(44, 1, 'User.1.45.jpg'),
(45, 1, 'User.1.46.jpg'),
(46, 1, 'User.1.47.jpg'),
(47, 1, 'User.1.48.jpg'),
(48, 1, 'User.1.49.jpg'),
(49, 1, 'User.1.50.jpg'),
(50, 1, 'User.1.51.jpg'),
(51, 1, 'User.1.52.jpg'),
(52, 1, 'User.1.53.jpg'),
(53, 1, 'User.1.54.jpg'),
(54, 1, 'User.1.55.jpg'),
(55, 1, 'User.1.56.jpg'),
(56, 1, 'User.1.57.jpg'),
(57, 1, 'User.1.58.jpg'),
(58, 1, 'User.1.59.jpg'),
(59, 1, 'User.1.60.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `ph_hmo`
--

CREATE TABLE `ph_hmo` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `district` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ph_hmo`
--

INSERT INTO `ph_hmo` (`id`, `name`, `mobile`, `email`, `district`, `uname`, `pass`) VALUES
(1, 'Girish', 9894442716, 'bgeduscanner@gmail.com', 'Salem', 'HM1', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `ph_hospital`
--

CREATE TABLE `ph_hospital` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `area` varchar(30) NOT NULL,
  `district` varchar(30) NOT NULL,
  `phc_id` varchar(20) NOT NULL,
  `detail` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ph_hospital`
--

INSERT INTO `ph_hospital` (`id`, `name`, `area`, `district`, `phc_id`, `detail`) VALUES
(1, 'GH1', 'Chatram', 'Thanjavur', 'P001', 'new google.maps.LatLng(10.835841,78.68845), new google.maps.LatLng(10.836531,78.68829), new google.maps.LatLng(10.836963,78.688456), new google.maps.LatLng(10.837063,78.689185), new google.maps.LatLng(10.835983,78.690022), new google.maps.LatLng(10.835704,78.689802), new google.maps.LatLng(10.835409,78.689062), new google.maps.LatLng(10.835841,78.68845), ');

-- --------------------------------------------------------

--
-- Table structure for table `ph_logs`
--

CREATE TABLE `ph_logs` (
  `id` int(11) NOT NULL,
  `doctor` varchar(20) NOT NULL,
  `docid` varchar(20) NOT NULL,
  `phc_id` varchar(20) NOT NULL,
  `status` varchar(30) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `rtime` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ph_logs`
--

INSERT INTO `ph_logs` (`id`, `doctor`, `docid`, `phc_id`, `status`, `rdate`, `rtime`) VALUES
(1, 'Dr. P.Raman, MBBS', 'D1', 'P001', 'Inside Hospital', '18-12-2025', '18:41:31'),
(2, 'Dr. P.Raman, MBBS', 'D1', 'P001', 'Outside Hospital', '18-12-2025', '18:47:57'),
(3, 'Dr. P.Raman, MBBS', 'D1', 'P001', 'Inside Hospital', '22-12-2025', '16:50:11');

-- --------------------------------------------------------

--
-- Table structure for table `ph_patient`
--

CREATE TABLE `ph_patient` (
  `id` int(11) NOT NULL,
  `docid` varchar(20) NOT NULL,
  `phc_id` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `age` int(11) NOT NULL,
  `aadhar` varchar(20) NOT NULL,
  `disease` varchar(50) NOT NULL,
  `symptom` varchar(50) NOT NULL,
  `prescribe` varchar(100) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `month` int(11) NOT NULL,
  `year` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ph_patient`
--

INSERT INTO `ph_patient` (`id`, `docid`, `phc_id`, `name`, `gender`, `age`, `aadhar`, `disease`, `symptom`, `prescribe`, `rdate`, `month`, `year`) VALUES
(1, 'D1', 'P001', 'Raji', 'Female', 45, '235856555588', 'Fever', 'cold, pain', 'Aspirin - 100mg, Morning-Night, for 3 days', '2025-04-06', 4, 2025);
