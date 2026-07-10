-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 15, 2025 at 10:49 AM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `health`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `auth_group`
--


-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `auth_group_permissions`
--


-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=25 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add permission', 2, 'add_permission'),
(5, 'Can change permission', 2, 'change_permission'),
(6, 'Can delete permission', 2, 'delete_permission'),
(7, 'Can add group', 3, 'add_group'),
(8, 'Can change group', 3, 'change_group'),
(9, 'Can delete group', 3, 'delete_group'),
(10, 'Can add user', 4, 'add_user'),
(11, 'Can change user', 4, 'change_user'),
(12, 'Can delete user', 4, 'delete_user'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add ymodel', 7, 'add_ymodel'),
(20, 'Can change ymodel', 7, 'change_ymodel'),
(21, 'Can delete ymodel', 7, 'delete_ymodel'),
(22, 'Can add emodel', 8, 'add_emodel'),
(23, 'Can change emodel', 8, 'change_emodel'),
(24, 'Can delete emodel', 8, 'delete_emodel');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `auth_user`
--


-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_30a071c9_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `auth_user_groups`
--


-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `auth_user_user_permissions`
--


-- --------------------------------------------------------

--
-- Table structure for table `calories`
--

CREATE TABLE IF NOT EXISTS `calories` (
  `calid` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(100) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `calories` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`calid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=31 ;

--
-- Dumping data for table `calories`
--

INSERT INTO `calories` (`calid`, `fname`, `amount`, `calories`) VALUES
(1, 'Chapatis', '100', '300'),
(2, 'Cornflakes', '100', '370'),
(3, 'Noodles', '100', '70'),
(4, 'Chicken', '100', '200'),
(5, 'Duck roast', '100', '430'),
(6, 'Beef (roast)', '100', '280'),
(7, 'Prawns', '100', '100'),
(8, 'Pork', '100', '290'),
(9, 'Apple', '100', '44'),
(10, 'Banana', '100', '65'),
(11, 'Cabbage (boiled)', '100', '20'),
(12, 'Carrot (boiled)', '100', '25'),
(13, 'Cauliflower (boiled)', '100', '30'),
(14, 'Cherry', '100', '50'),
(15, 'Cucumber', '100', '10'),
(16, 'Dates', '100', '235'),
(17, 'Grapes', '100', '62'),
(18, 'Kiwi', '100', '50'),
(19, 'Olives', '100', '80'),
(20, 'Orange', '100', '30'),
(21, 'Peas', '100', '148'),
(22, 'Pineapple', '100', '40'),
(23, 'Tomato', '100', '20'),
(24, 'Custard', '100', '100'),
(25, 'Ice cream', '100', '180'),
(26, 'corn', '100', '400'),
(27, 'wheat', '100', '1000'),
(28, 'kalki', '100', '1000'),
(29, 'Carrot', '100 gm', '41'),
(30, 'Rice ', '100 gm', '130');

-- --------------------------------------------------------

--
-- Table structure for table `chatm`
--

CREATE TABLE IF NOT EXISTS `chatm` (
  `chid` int(4) NOT NULL AUTO_INCREMENT,
  `uid` int(3) NOT NULL,
  `cdate` date NOT NULL,
  PRIMARY KEY (`chid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `chatm`
--

INSERT INTO `chatm` (`chid`, `uid`, `cdate`) VALUES
(1, 8, '2022-04-13'),
(2, 11, '2022-04-14'),
(3, 10, '2022-04-14'),
(4, 12, '2022-04-14'),
(5, 11, '2022-05-06');

-- --------------------------------------------------------

--
-- Table structure for table `chats`
--

CREATE TABLE IF NOT EXISTS `chats` (
  `ctid` int(11) NOT NULL AUTO_INCREMENT,
  `chat_id` int(4) NOT NULL,
  `msg` varchar(6000) NOT NULL,
  `typ` varchar(20) NOT NULL,
  PRIMARY KEY (`ctid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `chats`
--

INSERT INTO `chats` (`ctid`, `chat_id`, `msg`, `typ`) VALUES
(1, 1, ' hi', 'D'),
(2, 1, ' hi doc', 'U'),
(3, 1, ' exercise', 'D'),
(4, 2, ' Hello ', 'U'),
(5, 3, ' hello', 'U'),
(6, 4, ' hello', 'U'),
(7, 5, ' hello sir', 'U');

-- --------------------------------------------------------

--
-- Table structure for table `dietchild`
--

CREATE TABLE IF NOT EXISTS `dietchild` (
  `CDTID` int(11) NOT NULL AUTO_INCREMENT,
  `DTID` int(11) DEFAULT NULL,
  `DAY` varchar(20) DEFAULT NULL,
  `PBF` varchar(100) DEFAULT NULL,
  `BF` varchar(100) DEFAULT NULL,
  `BR` varchar(100) DEFAULT NULL,
  `LU` varchar(100) DEFAULT NULL,
  `EV` varchar(100) DEFAULT NULL,
  `DN` varchar(100) DEFAULT NULL,
  `TNOT` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`CDTID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=20 ;

--
-- Dumping data for table `dietchild`
--

INSERT INTO `dietchild` (`CDTID`, `DTID`, `DAY`, `PBF`, `BF`, `BR`, `LU`, `EV`, `DN`, `TNOT`) VALUES
(1, 1, '2021-06-13', 'a', 'fgtdfg', 'c', 'fdg', 'vc', 'di', 'ffff'),
(2, 1, '2021-06-05', 'a', 'y', 'y', 'y', 'y', 'y', 'y'),
(3, 2, '', '', '', '', '', '', '', ''),
(4, 2, '', 'sdf', 'dfdsf', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf'),
(5, 3, '2021-07-01', 'sxfd', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf'),
(6, 3, '2021-07-01', 'sxfd', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf'),
(7, 3, '2021-07-01', 'sxfd', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf'),
(8, 3, '2021-07-01', 'sxfd', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf'),
(9, 3, '2021-07-02', 'fsdf', 'sf', 'sfd', 'sdf', 'sdf', 'sdf', 'sdf'),
(10, 4, '2021-06-26', 'dfg', 'dfg', 'dfg', 'dfg', 'dg', 'dg', 'dfg'),
(11, 2, '2021-06-27', 'sdf', 'sdf', 'SDF', 'SDF', 'SFD', 'SDF', 'SDF'),
(12, 3, '2021-07-16', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf'),
(13, 4, '2021-07-14', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'sdf', 'dsf'),
(14, 7, 'AllDays', 'lime juice', 'chapathi', 'tea', 'dosa', 'cheese', 'salad', 'exercise'),
(15, 9, 'AllDays', '', '', '', '', '', '', ''),
(16, 10, 'AllDays', '', '', '', '', '', '', ''),
(17, 11, 'AllDays', '', '', '', '', '', '', ''),
(18, 14, 'AllDays', 'sss', 'wss', 'ss', 'sss', 'AA', 'sssss', 'fgd'),
(19, 15, 'AllDays', 'sss', 'wss', 'ss', 'sss', 'AA', 'sssss', 'ghgh');

-- --------------------------------------------------------

--
-- Table structure for table `dietmaster`
--

CREATE TABLE IF NOT EXISTS `dietmaster` (
  `DTID` int(11) NOT NULL AUTO_INCREMENT,
  `SDATE` date DEFAULT NULL,
  `EDATE` date DEFAULT NULL,
  `NOD` int(11) DEFAULT NULL,
  `RQID` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`DTID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

--
-- Dumping data for table `dietmaster`
--

INSERT INTO `dietmaster` (`DTID`, `SDATE`, `EDATE`, `NOD`, `RQID`) VALUES
(1, '2021-06-06', '2021-06-10', 5, '1'),
(2, '2021-06-27', '2021-07-03', 7, '1'),
(3, '2021-07-01', '2021-07-07', 7, '1'),
(4, '2021-06-26', '2021-06-30', 5, '2'),
(5, '2021-07-14', '2021-07-19', 5, '3'),
(6, '2021-07-14', '2021-07-18', 5, '4'),
(7, '2022-04-18', '2022-04-22', 5, '7'),
(8, '2022-04-13', '2022-04-20', 7, '5'),
(9, '2022-04-14', '2022-04-21', 7, '8'),
(10, '2022-04-14', '2022-04-21', 7, '9'),
(11, '2022-04-14', '2022-04-21', 7, '5'),
(12, '2022-05-04', '2022-05-12', 8, '10'),
(13, '2025-05-23', '2025-06-04', 9, '12'),
(14, '2025-05-16', '2025-05-17', 1, '12'),
(15, '2025-05-16', '2025-05-18', 2, '13');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_5151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_1c5f563_fk_auth_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `django_admin_log`
--


-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(8, 'MyApp', 'emodel'),
(7, 'MyApp', 'ymodel'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2022-04-12 21:18:45'),
(2, 'auth', '0001_initial', '2022-04-12 21:18:50'),
(3, 'admin', '0001_initial', '2022-04-12 21:18:51'),
(4, 'contenttypes', '0002_remove_content_type_name', '2022-04-12 21:18:51'),
(5, 'auth', '0002_alter_permission_name_max_length', '2022-04-12 21:18:52'),
(6, 'auth', '0003_alter_user_email_max_length', '2022-04-12 21:18:52'),
(7, 'auth', '0004_alter_user_username_opts', '2022-04-12 21:18:52'),
(8, 'auth', '0005_alter_user_last_login_null', '2022-04-12 21:18:52'),
(9, 'auth', '0006_require_contenttypes_0002', '2022-04-12 21:18:52'),
(10, 'sessions', '0001_initial', '2022-04-12 21:18:53');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('9luhu9it78kbf4gcimk4vgf7dfixvnqm', '.eJyrVgr1dFGyUjJS0lEK9XP0dQWyE4uySvOKE7MS84wc0nMTM3P0kvNzQfIBjsHB4f5BLjA1DoZGxiDxkMgAkL7S4tQipVoA3W8YOQ:1tuolb:82mVMXToRo2yKIo11-xzx8v0hyg3hAnDFiuEjcGFFB4', '2025-04-02 08:27:11'),
('adbltic4nch4cig5hrzj568h0gzxuasr', 'eyJzdGF0dXMiOiJwYWlkIn0:1uFW9a:-PrMp0tAG_BZOvpBILRKbRlAVxOG-iELEZa2d69jXDM', '2025-05-29 10:49:30'),
('bxis74xopo9shwmr8o6t8a125e8e82z8', 'OWFlYWU5Y2U0OGUyNjkyYzMzMmQ2YThkZDZiMWY5Y2Q5ZWY0MDAxNjp7fQ==', '2022-05-23 22:05:33'),
('cdrayt6f3q1qlqa4kfa0fx505i49ver5', '.eJyrViouSSwpLVayUlLSUQr1dAEyDA1BTD9HX1cgpygz0SE9NzEzRy85PxckHuAYHBzuH-QCkStJLUotTgSJh0QGgNSXFqcWKdUCAEZSGaI:1uF5mj:DU93yI12iR219duVc3QQCQa7zdKLLCYtxkMVglQeI9o', '2025-05-28 06:40:09'),
('eyfw128sbfv2jj44049dqk002x9dhl17', 'OWFlYWU5Y2U0OGUyNjkyYzMzMmQ2YThkZDZiMWY5Y2Q5ZWY0MDAxNjp7fQ==', '2022-04-27 03:00:29'),
('fa0hh8iyfkosctl2anq4p2nyevdwbf2v', '.eJyrViouSSwpLVayUipIzExR0lEK9XQBcgwNQUw_R19XIKcoM9EhPTcxM0cvOT8XJB7gGBwc7h_kApErSS1KLU4EiYdEBoDUlxanFinVAgDUUxtA:1uFSmc:lO7djdHTO2V50B7jrUPXsqG5XzOvOg5sOTHTC_1KNXI', '2025-05-29 07:13:34'),
('frhz7xykneaavx2iex4hcuzmgu8ksug9', 'eyJzdGF0dXMiOiIifQ:1txkSS:glH3oztAL1PYEXowtO9H5NK1G8V8Jme2ikWfo3q70mo', '2025-04-10 10:27:32'),
('j19ojxowpylqcocgnrgbu3v83pc9nhbc', 'OWFlYWU5Y2U0OGUyNjkyYzMzMmQ2YThkZDZiMWY5Y2Q5ZWY0MDAxNjp7fQ==', '2022-05-20 13:09:18'),
('l5rqqjqlp5deoacqe2kjc3xz5zgdohqq', 'NWE3MGI0N2M2OGZmZjJmNTgyODE5ZDkwOGFiNTg0YWRmNWJjOTlmYTp7IlVUWVBFIjoidXNlciIsIlVOQU1FIjoicmlhQGdtYWlsLmNvbSIsIlVQQVNTV09SRCI6InJpYXRlcmVzYSIsIlVJRCI6IjExIn0=', '2022-05-20 06:38:00'),
('llas3z03olay81j68l5yj6zlb27c2nbu', '.eJyrViouSSwpLVayUlLSUQr1dAEyLEAsP0dfVyC7OC81I9EhPTcxM0cvOT8XJBPgGBwc7h_kApMFiYVEBoBUlxanFinVAgAEAhia:1tvUpd:EWw5-osIF2cT8hPqjaR8iMd1ZqGNfZEXrWcTfF_1D00', '2025-04-04 05:22:09'),
('oirmttcqlm53nlhxyki7f6x32jvud8n4', 'MGI1MzZlM2Y4ODY2OGJhMmZjNzM3MWU5MzQxNmJiYjVmNjY3YmRlNDp7IlVUWVBFIjoiYWRtaW4iLCJVTkFNRSI6ImFkbWluQGdtYWlsLmNvbSIsIlVQQVNTV09SRCI6IjEyMzQ1IiwiVUlEIjoiMSJ9', '2022-05-20 07:52:14'),
('sidp117kqual07rbd5q80t4eyryp3zv1', 'OWFlYWU5Y2U0OGUyNjkyYzMzMmQ2YThkZDZiMWY5Y2Q5ZWY0MDAxNjp7fQ==', '2022-04-28 05:17:57'),
('vhckea776aedh2e5wt8e77zkvlllvlew', '.eJyrVgr1dFGyUjJS0lEK9XP0dQWyE4uySvOKE7MS84wc0nMTM3P0kvNzQfIBjsHB4f5BLjA1DoZGxiDxkMgAkL7S4tQipVoA3W8YOQ:1tumt4:8bGJBHEwdDuCLiidGwgLs8hu4DD0XYKnqNRWwnWh9lY', '2025-04-02 06:26:46'),
('w2efj3iuh9vttl0e6vlwubf904883ojg', 'OWFlYWU5Y2U0OGUyNjkyYzMzMmQ2YThkZDZiMWY5Y2Q5ZWY0MDAxNjp7fQ==', '2022-04-28 10:24:21'),
('z8crtzizybzz91qfrhew4fwnbvljm7ti', '.eJyrViouSSwpLVayUipIzExR0lEK9XQBcoxALD9HX1cgO7EoqzSvODErMc_IIT03MTNHLzk_FyQf4BgcHO4f5AJT42BoZAwSD4kMAOkrLU4tUqoFALhJHWk:1tv8E0:2F7sNmKlSrhxb_kW5TmtitHGNPq-I-AUseCuULlygq4', '2025-04-03 05:13:48');

-- --------------------------------------------------------

--
-- Table structure for table `exercise`
--

CREATE TABLE IF NOT EXISTS `exercise` (
  `EXID` int(11) NOT NULL AUTO_INCREMENT,
  `UID` int(11) NOT NULL,
  `ENAME` varchar(100) DEFAULT NULL,
  `ETYPE` varchar(50) DEFAULT NULL,
  `EDESC` varchar(6000) DEFAULT NULL,
  `EVIDEO` varchar(6000) DEFAULT NULL,
  PRIMARY KEY (`EXID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `exercise`
--

INSERT INTO `exercise` (`EXID`, `UID`, `ENAME`, `ETYPE`, `EDESC`, `EVIDEO`) VALUES
(1, 11, 'sss', ' Balance', 'ff', 'video/hollow-hold-amanda_OucuJ2I.webp'),
(2, 12, 'ttt', ' Flexibility', 'tttt', 'video/FORWARD_jrEjJ2y.webp');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE IF NOT EXISTS `feedback` (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) DEFAULT NULL,
  `msg` varchar(6000) DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`fid`, `fname`, `msg`) VALUES
(1, 'P K Rahul', 'Wonderful Service'),
(2, 'Vineeth S Kumar', 'I had a good support.'),
(3, 'Nibin Job', 'Great'),
(4, '8', 'asdasd');

-- --------------------------------------------------------

--
-- Table structure for table `ftemp`
--

CREATE TABLE IF NOT EXISTS `ftemp` (
  `food` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ftemp`
--

INSERT INTO `ftemp` (`food`) VALUES
('Avocados'),
('Cauliflower'),
('Corn'),
('Grapes'),
('Peas'),
('Pumpkin'),
('Sugar Doughnuts'),
('Poha'),
('Tomato'),
('Brownie');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE IF NOT EXISTS `login` (
  `uid` varchar(10) NOT NULL,
  `uname` varchar(100) DEFAULT NULL,
  `upass` varchar(100) DEFAULT NULL,
  `utype` varchar(100) DEFAULT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`uid`, `uname`, `upass`, `utype`, `status`) VALUES
('1', 'admin@gmail.com', '12345', 'admin', ''),
('2', 'arjunsajan2@gmail.com', 'arjun@123', 'user', 'approve'),
('3', 'diet@gmail.com', 'diet', 'dietician', ''),
('5', 'anjalibubby555@gmail.com', 'anjali@123', 'user', ''),
('6', 'fhh@gmail.com', 'fgdf', 'user', ''),
('8', 'sneha@gmail.com', 'sneha', 'user', 'paid'),
('10', 'reethushaji116@gmail.com', 'reethu', 'user', 'paid'),
('11', 'ria@gmail.com', 'riateresa', 'user', 'paid'),
('12', 'aleesha@gmail.com', 'aleesha', 'user', 'paid');

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE IF NOT EXISTS `registration` (
  `RID` int(10) NOT NULL AUTO_INCREMENT,
  `FIRST_NAME` varchar(100) DEFAULT NULL,
  `LAST_NAME` varchar(100) DEFAULT NULL,
  `ADDRESS` varchar(100) DEFAULT NULL,
  `PHONE` varchar(10) DEFAULT NULL,
  `EMAIL` varchar(100) DEFAULT NULL,
  `GENDER` varchar(10) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `status` varchar(58) NOT NULL,
  PRIMARY KEY (`RID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=13 ;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`RID`, `FIRST_NAME`, `LAST_NAME`, `ADDRESS`, `PHONE`, `EMAIL`, `GENDER`, `DOB`, `status`) VALUES
(2, 'Arjun', 'Sajan', 'Kunathil House, Mechilpara, Trivandrum', '9544203910', 'arjunsajan2@gmail.com', 'Male', '2000-05-16', 'approve'),
(8, 'Sneha', 'A', 'Kochi', '9878657657', 'sneha@gmail.com', 'Female', '1991-01-21', 'paid'),
(9, 'Reethu', 'Shaji', '1/2223', '9847073569', 'reethushaji116@gmail.com', 'Female', '2001-06-11', ''),
(10, 'Reethu ', 'Shaji', '22/3456', '9847073569', 'reethushaji116@gmail.com', 'Female', '1990-01-01', 'paid'),
(11, 'Ria', 'Teresa', 'Palampalliparambil', '9895899856', 'ria@gmail.com', 'Female', '1998-06-03', 'paid'),
(12, 'Aleesha', 'vm', '22/3456', '9898789678', 'aleesha@gmail.com', 'Female', '2001-04-14', 'paid');

-- --------------------------------------------------------

--
-- Table structure for table `reqdietplan`
--

CREATE TABLE IF NOT EXISTS `reqdietplan` (
  `rqid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` varchar(10) DEFAULT NULL,
  `wght` varchar(20) DEFAULT NULL,
  `hght` varchar(20) DEFAULT NULL,
  `bmi` varchar(20) DEFAULT NULL,
  `res` varchar(20) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`rqid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=14 ;

--
-- Dumping data for table `reqdietplan`
--

INSERT INTO `reqdietplan` (`rqid`, `cid`, `wght`, `hght`, `bmi`, `res`, `status`) VALUES
(1, '5', '70', '165', '25.711664', 'Over Weight', 'Diet Plan Added'),
(2, '7', '56', '158', '22.4323', 'Normal Weight', 'Diet Plan Added'),
(3, '8', '56', '158', '22.4323', 'Normal Weight', 'Diet Plan Added'),
(4, '8', '56', '158', '22.4323', 'Normal Weight', 'Diet Plan Added'),
(5, '8', '158.0', '56.0', '22.4323025156', 'Normal Weight', 'Diet Plan Added'),
(6, '8', '158.0', '70.0', '28.0403781445', 'Over Weight', 'Pending'),
(7, '10', '160.0', '67.0', '26.171875', 'Over Weight', 'Diet Plan Added'),
(8, '11', '156.0', '56.0', '23.0111768573', 'Normal Weight', 'Diet Plan Added'),
(9, '10', '130.0', '44.0', '26.0355029586', 'Over Weight', 'Diet Plan Added'),
(10, '12', '156.0', '50.0', '20.5456936226', 'Normal Weight', 'Request Sent'),
(11, '11', '154.0', '50.0', '21.0828132906', 'Normal Weight', 'Request Sent'),
(12, '12', '155.0', '50.0', '20.811654526534856', 'Normal Weight', 'Diet Plan Added'),
(13, '12', '155.0', '50.0', '20.811654526534856', 'Normal Weight', 'Diet Plan Added');

-- --------------------------------------------------------

--
-- Table structure for table `temp`
--

CREATE TABLE IF NOT EXISTS `temp` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `totalcalorie` varchar(20) DEFAULT NULL,
  `calid` varchar(20) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `temp`
--

INSERT INTO `temp` (`tid`, `totalcalorie`, `calid`, `amount`) VALUES
(1, '600.0', '1', '200');

-- --------------------------------------------------------

--
-- Table structure for table `yoga`
--

CREATE TABLE IF NOT EXISTS `yoga` (
  `YID` int(11) NOT NULL AUTO_INCREMENT,
  `UID` int(11) NOT NULL,
  `YNAME` varchar(100) DEFAULT NULL,
  `YTYPE` varchar(50) DEFAULT NULL,
  `YDESC` varchar(6000) DEFAULT NULL,
  `YPIC` varchar(6000) DEFAULT NULL,
  PRIMARY KEY (`YID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `yoga`
--

INSERT INTO `yoga` (`YID`, `UID`, `YNAME`, `YTYPE`, `YDESC`, `YPIC`) VALUES
(1, 11, 'aaa', 'Weight Gain', 'hh', 'pictures/2_24self.webp'),
(2, 12, 'hhh', 'Weight Gain', 'hhhh', 'pictures/Francine-lateral-lunge_xwJvqqv.gif');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissions_group_id_58c48ba9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permissi_content_type_id_51277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_30a071c9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_24702650_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permissions_user_id_7cd7acb6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_user_id_1c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `django_admin__content_type_id_5151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

-- --------------------------------------------------------

--
-- Table structure for table `youtube_videos`
-- (Required by userhome and addyoutube views)
--

CREATE TABLE IF NOT EXISTS `youtube_videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `youtube_videos`
--

