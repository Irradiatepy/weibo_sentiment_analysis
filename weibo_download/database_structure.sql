/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50623
Source Host           : localhost:3306
Source Database       : weibo2

Target Server Type    : MYSQL
Target Server Version : 50623
File Encoding         : 65001

Date: 2015-06-25 21:08:41
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `detailprofile`
-- ----------------------------
DROP TABLE IF EXISTS `detailprofile`;
CREATE TABLE `detailprofile` (
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`gender`  int(11) NULL DEFAULT NULL ,
`description`  varchar(160) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`address`  varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`birthday`  varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`blog`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`relation`  varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`sexuality`  int(11) NULL DEFAULT NULL ,
`bloodtype`  varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`fashion`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`weiboid`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `dlut`
-- ----------------------------
DROP TABLE IF EXISTS `dlut`;
CREATE TABLE `dlut` (
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`is_profile`  int(11) NULL DEFAULT NULL ,
`is_wb_ori_no_pic`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`weiboid`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `dlut_wordsegment`
-- ----------------------------
DROP TABLE IF EXISTS `dlut_wordsegment`;
CREATE TABLE `dlut_wordsegment` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`segments`  varchar(480) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`keywords`  varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`is_meaningful`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `ecupsl`
-- ----------------------------
DROP TABLE IF EXISTS `ecupsl`;
CREATE TABLE `ecupsl` (
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`is_profile`  int(11) NULL DEFAULT NULL ,
`is_wb_ori_no_pic`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`weiboid`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `ecupsl_wb_ori_no_pic`
-- ----------------------------
DROP TABLE IF EXISTS `ecupsl_wb_ori_no_pic`;
CREATE TABLE `ecupsl_wb_ori_no_pic` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ftime`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`content`  varchar(320) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`upvotes`  int(11) NULL DEFAULT NULL ,
`forwards`  int(11) NULL DEFAULT NULL ,
`reviews`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `ecupsl_wordsegment`
-- ----------------------------
DROP TABLE IF EXISTS `ecupsl_wordsegment`;
CREATE TABLE `ecupsl_wordsegment` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`segments`  varchar(480) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`keywords`  varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`is_meaningful`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `education`
-- ----------------------------
DROP TABLE IF EXISTS `education`;
CREATE TABLE `education` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`school`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`enrolltime`  varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `full_user_weibo`
-- ----------------------------
DROP TABLE IF EXISTS `full_user_weibo`;
CREATE TABLE `full_user_weibo` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ftime`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`content`  varchar(320) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`upvotes`  int(11) NULL DEFAULT NULL ,
`forwards`  int(11) NULL DEFAULT NULL ,
`reviews`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `markedweibo`
-- ----------------------------
DROP TABLE IF EXISTS `markedweibo`;
CREATE TABLE `markedweibo` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`content`  varchar(320) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`mark`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `nanking`
-- ----------------------------
DROP TABLE IF EXISTS `nanking`;
CREATE TABLE `nanking` (
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`is_profile`  int(11) NULL DEFAULT NULL ,
`is_wb_ori_no_pic`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`weiboid`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `nanking_wb_ori_no_pic`
-- ----------------------------
DROP TABLE IF EXISTS `nanking_wb_ori_no_pic`;
CREATE TABLE `nanking_wb_ori_no_pic` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ftime`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`content`  varchar(320) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`upvotes`  int(11) NULL DEFAULT NULL ,
`forwards`  int(11) NULL DEFAULT NULL ,
`reviews`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `nanking_wordsegment`
-- ----------------------------
DROP TABLE IF EXISTS `nanking_wordsegment`;
CREATE TABLE `nanking_wordsegment` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`segments`  varchar(480) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`keywords`  varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`is_meaningful`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `peking`
-- ----------------------------
DROP TABLE IF EXISTS `peking`;
CREATE TABLE `peking` (
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`is_profile`  int(11) NULL DEFAULT NULL ,
`is_wb_ori_no_pic`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`weiboid`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `peking_wb_ori_no_pic`
-- ----------------------------
DROP TABLE IF EXISTS `peking_wb_ori_no_pic`;
CREATE TABLE `peking_wb_ori_no_pic` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ftime`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`content`  varchar(320) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`upvotes`  int(11) NULL DEFAULT NULL ,
`forwards`  int(11) NULL DEFAULT NULL ,
`reviews`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `peking_wordsegment`
-- ----------------------------
DROP TABLE IF EXISTS `peking_wordsegment`;
CREATE TABLE `peking_wordsegment` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`segments`  varchar(480) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`keywords`  varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`is_meaningful`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `profile`
-- ----------------------------
DROP TABLE IF EXISTS `profile`;
CREATE TABLE `profile` (
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
`nickname`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`is_education`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`weiboid`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `tsinghua`
-- ----------------------------
DROP TABLE IF EXISTS `tsinghua`;
CREATE TABLE `tsinghua` (
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`is_profile`  int(11) NULL DEFAULT NULL ,
`is_wb_ori_no_pic`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`weiboid`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `tsinghua_wb_ori_no_pic`
-- ----------------------------
DROP TABLE IF EXISTS `tsinghua_wb_ori_no_pic`;
CREATE TABLE `tsinghua_wb_ori_no_pic` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ftime`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`content`  varchar(320) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`upvotes`  int(11) NULL DEFAULT NULL ,
`forwards`  int(11) NULL DEFAULT NULL ,
`reviews`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `tsinghua_wordsegment`
-- ----------------------------
DROP TABLE IF EXISTS `tsinghua_wordsegment`;
CREATE TABLE `tsinghua_wordsegment` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`segments`  varchar(480) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`keywords`  varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`is_meaningful`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Table structure for `wb_ori_no_pic`
-- ----------------------------
DROP TABLE IF EXISTS `wb_ori_no_pic`;
CREATE TABLE `wb_ori_no_pic` (
`wmd5`  varchar(48) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' ,
`weiboid`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`ftime`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`content`  varchar(320) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`upvotes`  int(11) NULL DEFAULT NULL ,
`forwards`  int(11) NULL DEFAULT NULL ,
`reviews`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`wmd5`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;
