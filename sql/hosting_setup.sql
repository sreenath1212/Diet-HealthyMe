-- ============================================================
-- HOSTING DATABASE SETUP SCRIPT
-- Run this on your hosting MySQL (e.g. via phpMyAdmin)
-- This adds tables that may have been created only in WAMP
-- ============================================================

-- YouTube videos table (used by userhome and addyoutube views)
CREATE TABLE IF NOT EXISTS `youtube_videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Django session table (required for sessions to work)
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Django content types (required for admin)
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Django migrations tracking table
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Auth permission table
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Auth group table
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Django admin log table
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Auth user table (for Django admin login)
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ============================================================
-- CORE APPLICATION TABLES
-- These MUST exist for the app to work
-- ============================================================

CREATE TABLE IF NOT EXISTS `registration` (
  `RID` int(10) NOT NULL AUTO_INCREMENT,
  `FIRST_NAME` varchar(100) DEFAULT NULL,
  `LAST_NAME` varchar(100) DEFAULT NULL,
  `ADDRESS` varchar(100) DEFAULT NULL,
  `PHONE` varchar(10) DEFAULT NULL,
  `EMAIL` varchar(100) DEFAULT NULL,
  `GENDER` varchar(10) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `status` varchar(58) NOT NULL DEFAULT '',
  PRIMARY KEY (`RID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `login` (
  `uid` varchar(10) NOT NULL,
  `uname` varchar(100) DEFAULT NULL,
  `upass` varchar(200) DEFAULT NULL,
  `utype` varchar(100) DEFAULT NULL,
  `status` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `registration` (
  `RID` int(10) NOT NULL AUTO_INCREMENT,
  `FIRST_NAME` varchar(100) DEFAULT NULL,
  `LAST_NAME` varchar(100) DEFAULT NULL,
  `ADDRESS` varchar(100) DEFAULT NULL,
  `PHONE` varchar(10) DEFAULT NULL,
  `EMAIL` varchar(100) DEFAULT NULL,
  `GENDER` varchar(10) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `status` varchar(58) NOT NULL DEFAULT '',
  PRIMARY KEY (`RID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `reqdietplan` (
  `rqid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` varchar(10) DEFAULT NULL,
  `wght` varchar(20) DEFAULT NULL,
  `hght` varchar(20) DEFAULT NULL,
  `bmi` varchar(20) DEFAULT NULL,
  `res` varchar(20) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`rqid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `dietmaster` (
  `DTID` int(11) NOT NULL AUTO_INCREMENT,
  `SDATE` date DEFAULT NULL,
  `EDATE` date DEFAULT NULL,
  `NOD` int(11) DEFAULT NULL,
  `RQID` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`DTID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `exercise` (
  `EXID` int(11) NOT NULL AUTO_INCREMENT,
  `UID` int(11) NOT NULL,
  `ENAME` varchar(100) DEFAULT NULL,
  `ETYPE` varchar(50) DEFAULT NULL,
  `EDESC` varchar(6000) DEFAULT NULL,
  `EVIDEO` varchar(6000) DEFAULT NULL,
  PRIMARY KEY (`EXID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `yoga` (
  `YID` int(11) NOT NULL AUTO_INCREMENT,
  `UID` int(11) NOT NULL,
  `YNAME` varchar(100) DEFAULT NULL,
  `YTYPE` varchar(50) DEFAULT NULL,
  `YDESC` varchar(6000) DEFAULT NULL,
  `YPIC` varchar(6000) DEFAULT NULL,
  PRIMARY KEY (`YID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `calories` (
  `calid` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(100) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `calories` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`calid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `chatm` (
  `chid` int(4) NOT NULL AUTO_INCREMENT,
  `uid` int(3) NOT NULL,
  `cdate` date NOT NULL,
  PRIMARY KEY (`chid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `chats` (
  `ctid` int(11) NOT NULL AUTO_INCREMENT,
  `chat_id` int(4) NOT NULL,
  `msg` varchar(6000) NOT NULL,
  `typ` varchar(20) NOT NULL,
  PRIMARY KEY (`ctid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `ftemp` (
  `food` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `feedback` (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) DEFAULT NULL,
  `msg` varchar(6000) DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `youtube_videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
