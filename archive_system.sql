-- MySQL dump 10.13  Distrib 9.0.1, for macos15.1 (arm64)
--
-- Host: localhost    Database: archive_system
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailaddress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_upper` ((upper(`email`))),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
INSERT INTO `account_emailaddress` VALUES (1,'admin@admin.com',1,1,1),(14,'test4@test.com',1,1,9),(15,'syun100000@gmail.com',1,1,10),(16,'staff@staff.com',1,1,11),(17,'test@test.com',1,1,12),(18,'test3@test.com',1,1,13);
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_address_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$870000$0CkTbm9MjLYzoAO58bEDza$gUJndZKKFiP2c/bD5WOlnxTqgyrRwsFkR0Q9/6j23iU=','2024-10-30 04:36:35.698801','admin@admin.com','admin','admin',1,1,1,'2024-06-14 08:15:51.302291'),(9,'pbkdf2_sha256$600000$NprACQKytlY7pv1h7ia11u$roAq0a9c+K7EuQLkJvCHj96/7Bnt8jDnA9SmuIMug+Y=','2024-07-02 04:38:04.573601','test4@test.com','','',1,0,0,'2024-07-02 04:37:56.168756'),(10,'pbkdf2_sha256$600000$2ZozrJ3p2stFRvrVwjeTPn$XW7FB6t5/zPl1y0AiSM+WFC73G16/+rj75N/LuV6Z08=','2024-07-02 07:22:04.649952','syun100000@gmail.com','斎藤','隼佑',1,1,1,'2024-07-02 07:04:22.474667'),(11,'pbkdf2_sha256$870000$FDHMjqG3iNLLBk1OKR0hvB$6C8LL3AFQEkySwRsn8HMa4fzSKi1Alq72Xl+4MBJvoA=','2024-10-30 04:35:20.755993','staff@staff.com','staff','staff',1,1,0,'2024-08-08 07:22:35.690153'),(12,'pbkdf2_sha256$600000$s5Y9xEcUMYTnlLVlF5zu9I$MyGzjnw45khHJ5M6JLkMOd4wSK8Fk3hfiqGUppulwXQ=',NULL,'test@test.com','','',1,0,0,'2024-08-08 07:23:32.233696'),(13,'pbkdf2_sha256$870000$eez0VFjO6K2YV8mtKZ2P4u$vrMAx8qi4uxjxNGQAJQr2rSHxKFuFUIlkQSy3bn18Z4=','2024-10-16 08:09:25.854838','test3@test.com','test','test',1,0,0,'2024-10-16 08:08:27.519104'),(14,'pbkdf2_sha256$870000$uzugIEg3zF76wTk4uenLxF$iirXbgOUHzpGEBBz+nzY0HNaxdBkCdzviOj16Be8Gt8=',NULL,'admin1@admin.com','admin','admin',1,0,0,'2024-10-16 08:30:34.268274');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveViewer_announcement`
--

DROP TABLE IF EXISTS `ArchiveViewer_announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ArchiveViewer_announcement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `created_by_id` bigint NOT NULL,
  `deleted_by_id` bigint DEFAULT NULL,
  `updated_by_id` bigint NOT NULL,
  `is_html` tinyint(1) NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ArchiveViewer_announ_created_by_id_391a1bfd_fk_accounts_` (`created_by_id`),
  KEY `ArchiveViewer_announ_deleted_by_id_7b2f1986_fk_accounts_` (`deleted_by_id`),
  KEY `ArchiveViewer_announ_updated_by_id_13f1db1a_fk_accounts_` (`updated_by_id`),
  CONSTRAINT `ArchiveViewer_announ_created_by_id_391a1bfd_fk_accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `ArchiveViewer_announ_deleted_by_id_7b2f1986_fk_accounts_` FOREIGN KEY (`deleted_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `ArchiveViewer_announ_updated_by_id_13f1db1a_fk_accounts_` FOREIGN KEY (`updated_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveViewer_announcement`
--

LOCK TABLES `ArchiveViewer_announcement` WRITE;
/*!40000 ALTER TABLE `ArchiveViewer_announcement` DISABLE KEYS */;
INSERT INTO `ArchiveViewer_announcement` VALUES (1,'テスト','テスト','2024-05-20 14:41:25.137318','2024-05-20 14:53:32.047492',1,1,NULL,1,0,0),(2,'って','て','2024-05-22 08:44:51.882904','2024-05-23 06:16:07.706635',1,1,NULL,1,0,0),(3,'ｒｔｇｓ','ｇｆｓｄｆ','2024-05-22 08:45:17.806437','2024-05-23 06:16:07.701995',1,1,NULL,1,0,0),(4,'','','2024-05-22 17:46:39.650900','2024-05-23 06:16:07.682026',1,1,NULL,1,0,0),(5,'進修館オープンカレッジ「スキップ広場に賑わいを！」参加者募集！','進修館では、地域の皆様に向けてオープンカレッジ「スキップ広場に賑わいを！」を開催いたします。今回のカレッジでは、地域の活性化をテーマに、様々なワークショップや講演を予定しております。皆様のご参加をお待ちしております。','2024-05-23 06:17:31.844730','2024-10-16 08:45:12.392602',0,1,NULL,1,0,1),(6,'【お知らせ】新しい図書館システム導入のお知らせ','<p>皆様</p>\r\n\r\n<p>平素より図書館をご利用いただき、誠にありがとうございます。この度、当館ではより良いサービスを提供するために、新しい図書館システムを導入いたしました。</p>\r\n\r\n<p>新システムの導入により、これまで以上に便利で快適な図書館利用が可能になります。以下に新システムの主な機能と利点を紹介いたします。</p>\r\n\r\n<p>1. <strong>オンライン予約システムの導入</strong><br>\r\n新システムでは、インターネットを通じて図書の予約ができるようになります。これにより、来館前にお目当ての書籍を確実に確保できるほか、予約の状況をリアルタイムで確認することができます。利用者は自宅や職場から簡単に予約ができ、効率的に図書館をご利用いただけます。</p>\r\n\r\n<p>2. <strong>電子書籍の拡充</strong><br>\r\n新システムでは、従来の紙の書籍に加えて、電子書籍の貸し出しサービスも開始します。スマートフォンやタブレット、パソコンなどの端末から電子書籍を閲覧できるため、外出先でも快適に読書を楽しむことができます。電子書籍のラインナップも充実させており、最新刊や話題の書籍も続々と追加予定です。</p>\r\n\r\n<p>3. <strong>自動貸出・返却システムの導入</strong><br>\r\n新システムでは、セルフサービスによる貸出・返却が可能になります。これにより、利用者は待ち時間を短縮でき、スムーズに図書を利用できます。また、返却期限の管理もシステムが自動で行うため、返却期限を忘れてしまう心配もありません。</p>\r\n\r\n<p>4. <strong>利用履歴の管理</strong><br>\r\n新システムでは、個人の利用履歴を管理し、過去に借りた書籍のリストを確認できるようになります。これにより、再度同じ本を借りる際の手間を省くことができます。また、お気に入りの書籍リストを作成し、次回の利用時に参考にすることも可能です。</p>\r\n\r\n<p>5. <strong>イベント情報の配信</strong><br>\r\n新システムでは、図書館で開催されるイベントや講演会の情報を配信する機能も追加されます。利用者はスマートフォンやメールで最新のイベント情報を受け取ることができ、興味のあるイベントにいち早く参加できます。</p>\r\n\r\n<p>新システムの導入に伴い、これまで以上に多くの方々に図書館を利用していただけるよう、スタッフ一同努めてまいります。何かご不明点やご質問がございましたら、図書館スタッフまでお気軽にお問い合わせください。</p>\r\n\r\n<p>今後とも、当図書館をご愛顧賜りますようお願い申し上げます。</p>\r\n\r\n<p>図書館長</p>','2024-06-12 16:14:14.264429','2024-10-16 08:45:12.375599',0,1,NULL,1,1,1),(7,'あ','<p>テスト</p>','2024-06-12 16:38:52.526380','2024-06-12 17:28:19.838409',1,1,NULL,1,1,0);
/*!40000 ALTER TABLE `ArchiveViewer_announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveViewer_report`
--

DROP TABLE IF EXISTS `ArchiveViewer_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ArchiveViewer_report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  `is_recommend` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `category_id` bigint DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `deleted_by_id` bigint DEFAULT NULL,
  `updated_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ArchiveViewer_report_category_id_91959c2e_fk_ArchiveVi` (`category_id`),
  KEY `ArchiveViewer_report_created_by_id_635b4133_fk_accounts_user_id` (`created_by_id`),
  KEY `ArchiveViewer_report_deleted_by_id_b5b9edf1_fk_accounts_user_id` (`deleted_by_id`),
  KEY `ArchiveViewer_report_updated_by_id_8cd8d28f_fk_accounts_user_id` (`updated_by_id`),
  CONSTRAINT `ArchiveViewer_report_category_id_91959c2e_fk_ArchiveVi` FOREIGN KEY (`category_id`) REFERENCES `ArchiveViewer_reportcategory` (`id`),
  CONSTRAINT `ArchiveViewer_report_created_by_id_635b4133_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `ArchiveViewer_report_deleted_by_id_b5b9edf1_fk_accounts_user_id` FOREIGN KEY (`deleted_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `ArchiveViewer_report_updated_by_id_8cd8d28f_fk_accounts_user_id` FOREIGN KEY (`updated_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveViewer_report`
--

LOCK TABLES `ArchiveViewer_report` WRITE;
/*!40000 ALTER TABLE `ArchiveViewer_report` DISABLE KEYS */;
INSERT INTO `ArchiveViewer_report` VALUES (3,'テスト','<p>ああああテスト</p>\r\n\r\n<p>テスト</p>\r\n',0,0,'2023-10-18 10:16:49.919662','2024-10-15 08:47:37.530507',0,NULL,1,NULL,1),(4,'Djangoにおけるモデルの利用方法','<p><cite><span dir=\"rtl\">Djangoでは、データベースと連携するためのモデルを作成することができる。このモデルはPythonのクラスとして定義され、データベースのテーブルと対応する。モデルを作成した後、マイグレーションを行い、データベースにテーブルを作成する。このプロセスを通じて、データのCRUD操作が容易になる。」とする。タグには「Django, モデル, データベース」を付ける。このテスト記事は、Djangoの基本的な機能と使い方について説明しているため、初心者にも理解しやすい内容となっている</span></cite></p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>&nbsp;</p>',1,1,'2023-10-18 13:06:59.991727','2023-11-10 17:29:55.842398',0,NULL,1,NULL,1),(6,'iPhone 15','<h1>iPhone15の記事</h1>\r\n\r\n<p>iPhone15は、Appleが2023年9月に発表した最新のスマートフォンです。iPhone15は、前モデルのiPhone14と比べて、どのような特徴や魅力があるのでしょうか？この記事では、iPhone15の主な仕様や機能、価格や発売日などを紹介します。</p>\r\n\r\n<h2>iPhone15の主な仕様</h2>\r\n\r\n<p>iPhone15は、6.1インチのOLEDディスプレイを搭載しています。ディスプレイは、ProMotion技術によって最大120Hzのリフレッシュレートを実現し、滑らかで快適な画面操作が可能です。また、True ToneやHDR10にも対応しており、色彩やコントラストが豊かに表現されます。</p>\r\n\r\n<p>iPhone15のカメラは、背面に1200万画素の広角レンズと望遠レンズ、超広角レンズの3つを備えています。広角レンズと望遠レンズは、光学式手ブレ補正と2倍の光学ズームに対応しており、安定した撮影ができます。超広角レンズは、F値1.8という明るいレンズで、夜景や暗所でも美しい写真が撮れます。また、カメラは、ナイトモードやポートレートモード、パノラマモードなどの様々な撮影モードに対応しており、シーンに合わせて最適な写真が撮れます。</p>\r\n\r\n<p>iPhone15のプロセッサは、Apple独自のA16 Bionicチップを採用しています。A16 Bionicチップは、5nmプロセスで製造された6コアのCPUと4コアのGPUを搭載しており、高いパフォーマンスと省電力性を両立しています。また、A16 Bionicチップは、ニューラルエンジンと呼ばれる16コアのAI処理部分も備えており、写真や動画の編集やゲームなどの高度な処理を高速に行えます。</p>\r\n\r\n<p>iPhone15のバッテリーは、前モデルよりも大容量になっており、最大18時間の連続使用が可能です。また、MagSafeという磁気式のワイヤレス充電に対応しており、専用の充電器やアクセサリーを使うことで便利に充電できます。</p>\r\n\r\n<h2>iPhone15の価格と発売日</h2>\r\n\r\n<p>iPhone15は、64GBモデルが9万9800円（税別）、128GBモデルが10万9800円（税別）、256GBモデルが12万4800円（税別）で販売されています。カラーバリエーションは、シルバー、グラファイト、ゴールド、パシフィックブルーの4色から選べます。</p>\r\n\r\n<p>iPhone15は、2023年9月24日に予約開始され、10月1日に発売されました。現在も各キャリアやオンラインストアで購入することができます。</p>\r\n\r\n<h2>まとめ</h2>\r\n\r\n<p>iPhone15は、高性能なプロセッサやカメラ、ディスプレイなどを備えたAppleの最新スマートフォンです。価格は高めですが、その分品質や機能性に優れています。iPhoneファンや最新技術に興味のある方には、ぜひおすすめしたい製品です。<br />\r\n&nbsp;</p>\r\n',1,1,'2023-10-20 05:29:44.940465','2024-08-24 07:51:47.077229',0,NULL,1,NULL,1),(7,'dddddd','<p>ddddd</p>',1,0,'2023-11-02 01:42:37.353112','2024-10-15 08:43:35.507024',0,NULL,1,NULL,1),(10,'かんたん！','<!-- テスト -->\r\n<div class=\"headline1\">\r\n<h2>テスト</h2>\r\n\r\n<p>これは簡単機能です。</p>\r\n</div>\r\n',1,0,'2023-11-08 05:12:41.126906','2024-08-22 08:28:09.389543',0,NULL,1,NULL,1),(11,'Vaundy 瞳惚れ','<h2 style=\"font-style:italic;\">&nbsp;</h2>\r\n\r\n<p data-sourcepos=\"3:1-3:77\">Vaundyの「瞳惚れ」は、2022年10月28日に配信リリースされた楽曲である。テレビ朝日系ドラマ「ジャパニーズスタイル」の主題歌として書き下ろされた。</p>\r\n\r\n<p data-sourcepos=\"5:1-5:59\">この曲は、恋に落ちてしまったときの、相手の瞳に吸い込まれていくような、目が離せないような、そんな感覚を歌った曲である。</p>\r\n\r\n<p data-sourcepos=\"7:1-7:56\">イントロのピアノの音色が、どこか懐かしさを感じさせる。そして、Vaundyの伸びやかな歌声が、聴く者の心を掴む。</p>\r\n\r\n<p data-sourcepos=\"9:1-9:61\">サビの「瞳に吸い込まれて、もう戻れない」というフレーズは、まさに恋に落ちてしまったときの、心が揺れ動く様子を表現している。</p>\r\n\r\n<p data-sourcepos=\"11:1-11:70\">また、この曲は、Vaundyの音楽的才能が存分に発揮された作品でもある。ポップなメロディーと、エモーショナルな歌詞が、絶妙にマッチしている。</p>\r\n\r\n<p data-sourcepos=\"13:1-13:39\">「瞳惚れ」は、恋に落ちたことがある人なら誰もが共感できる、心に響く楽曲である。</p>\r\n\r\n<p data-sourcepos=\"15:1-15:14\"><strong>Vaundyについて</strong></p>\r\n\r\n<p data-sourcepos=\"17:1-17:68\">Vaundyは、2019年にデビューしたシンガーソングライターである。2020年にリリースした楽曲「東京」がヒットし、一躍注目を集めた。</p>\r\n\r\n<p data-sourcepos=\"19:1-19:98\">Vaundyの音楽は、ポップ、ロック、R&amp;Bなど、さまざまなジャンルを融合させた、独自のスタイルが特徴である。また、Vaundy自身が作詞作曲を担当しており、その才能は高く評価されている。</p>\r\n\r\n<p data-sourcepos=\"21:1-21:74\">「瞳惚れ」は、Vaundyの代表曲のひとつである。この曲のヒットにより、Vaundyはさらに知名度を高め、日本の音楽シーンに欠かせない存在となった。</p>\r\n\r\n<p data-sourcepos=\"23:1-23:22\">今後も、Vaundyの活躍から目が離せない。</p>\r\n\r\n<p>さりげなく時は あの日まで流れ、着いた 鈍い足取りは 甘い香りに誘われて 突き刺す音で体が揺れる 予感がした まるで出会うことを知ってたかのように 今虜になっていく それはトキメクパッションで 滑り込んで、瞳奪っていく ほらまだ眩しいよ あれ、虜になっていく あの魅惑のパッションに 滑り込んできた小悪魔も ほら、踊り出して もう それは、目まぐるしく笑い 目を塞いでも、また思い出すように 眩暈がするほど強い光 言葉足らずの それは瞳惚れ あの日から時は 重くなり止まり出した 迷う秒針はあの日の魔法に惑わされ きっと 心がもたないね 煮詰まり思いが噴き出て しまいそうなほど 見間違いじゃないね 迷う秒針が焦って 巻き戻り出す前に 背けるたびに体が揺れる 予感がした それは逃げることを知ってたかのように また虜になっていく それはトキメクパッションで 滑り込んで、瞳奪っていく ほらまだ眩しいよ あれ、虜になっていく あの魅惑のパッションに 滑り込んできた小悪魔も ほら、踊り出して もう その瞳放つ、風邪で体が痺れる 予感がした 振り返れば時が進んでく 落ちるように 今虜になっていく それはトキメクパッションで 滑り込んで、瞳奪っていく ほらまだ眩しいよ あれ、虜になっていく あの魅惑のパッションに 滑り込んできた小悪魔も ほら、踊り出して もう それは、目まぐるしく笑い 目を塞いでも、また思い出すように 眩暈がするほど強い光 言葉足らずの それは瞳惚れ</p>\r\n\r\n<div class=\"text-center mt-4\">\r\n<audio controls=\"\"><source src=\"/media/01%20%E7%9E%B3%E6%83%9A%E3%82%8C.m4a\" type=\"audio/mp3\" /></audio>\r\n\r\n<p>01 瞳惚れ.m4a</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>&nbsp;</p>\r\n</div>',1,1,'2023-11-08 14:23:31.756777','2023-11-10 17:33:17.163658',0,NULL,1,NULL,1),(12,'テスト','<div class=\"headline1\">\r\n<h2>テスト見出し</h2>\r\n\r\n<p>テスト内容</p>\r\n</div>\r\n',0,0,'2023-11-09 01:37:17.274659','2024-08-26 16:39:56.508996',0,NULL,1,NULL,1),(13,'asdfdfsa','<div class=\"headline1\">\n    <h2>fdsafdsafsda</h2>\n    <p>sdfafdsda</p>\n</div>',0,0,'2023-11-09 04:26:01.034882','2023-11-09 04:26:01.034926',0,NULL,1,NULL,1),(14,'テスト投稿です','<p>これは2023/11/11投稿のテストです</p>',0,0,'2023-11-10 17:32:08.516047','2023-11-10 17:32:17.181231',0,NULL,1,NULL,1),(15,'現在でもビットコインマイニングは稼げるのでしょうか？','<p>ビットコインマイニングの収益性は、複数の要因に依存していますが、2023年時点で一定の利益を生む可能性があるとされています。1ブロックのマイニング報酬は6.25BTCであり、2023年8月のレートで1BTC＝約400万円の場合、1ブロックの取引記録に成功すれば約2,500万円の利益になると報告されています​​。しかし、2022年のビットコイン価格の下落により、マイニング収益も下がったという実績があり、2023年のマイニング収益が儲からないかどうかはマイニング難易度と価格の点から検討する必要があると指摘されています​​。一方で、2023年の仮想通貨マイニングが依然として収益性が高い可能性があるとも言われていますが、前年と比べ収益性のレベルが下がる可能性もあるとの見解が示されています​​。また、ASICマイニングは一定の収益性を保っているものの、2021年の高値と比べると収益性は低下しているという意見もあります​​。</p>\r\n\r\n<p>これらの情報を総合すると、ビットコインマイニングは依然として利益を生む可能性はあるものの、過去のデータと比較すると収益性は低下していることが予測されます。したがって、ビットコインマイニングへの投資は慎重に行い、現在の市場状況や電力コストなどを考慮する必要があります。</p>',1,0,'2023-11-10 17:41:22.663483','2023-11-10 17:41:22.663558',0,NULL,1,NULL,1),(16,'簡単とうこうでつくりました','<div class=\"headline1\">\n    <h2>テスト</h2>\n    <p>あｇぢおｒｓｇｊふぉいｄｓじょいｆｑじぇｒ＠「おうｑ0ーｒｇふぃ</p>\n</div>',0,0,'2023-11-16 01:26:48.049933','2023-11-16 01:26:48.049969',0,NULL,1,NULL,1),(28,'音楽','<div class=\"headline1\">\r\n<h2>着信音</h2>\r\n\r\n<p>着信音として用いている</p>\r\n\r\n<div class=\"contents\">\r\n<div class=\"content-item\">\r\n<audio class=\"audio-player\" controls=\"\" src=\"/media/%E3%83%A8%E3%83%BC%E3%83%86%E3%82%99%E3%83%AB%E9%A3%9F%E3%81%B8%E3%82%99%E6%94%BE%E9%A1%8C%20%E7%9D%80%E4%BF%A1%E9%9F%B3.mp3\">&nbsp;</audio>\r\n\r\n<p class=\"audio-name\">ヨーデル食べ放題 着信音.mp3</p>\r\n<a class=\"btn btn-primary\" href=\"/upload_contents_detail/75/\">コンテンツの詳細</a></div>\r\n</div>\r\n</div>\r\n\r\n<div class=\"headline2\">\r\n<h2>わがまま</h2>\r\n\r\n<p>ボーイのわがままジュリエット</p>\r\n\r\n<div class=\"contents\">\r\n<div class=\"content-item\">\r\n<audio class=\"audio-player\" controls=\"\" src=\"/media/1-07%20%E3%82%8F%E3%81%8B%E3%82%99%E3%81%BE%E3%81%BE%E3%82%B7%E3%82%99%E3%83%A5%E3%83%AA%E3%82%A8%E3%83%83%E3%83%88.mp3\">&nbsp;</audio>\r\n\r\n<p class=\"audio-name\">1-07 わがままジュリエット.mp3</p>\r\n<a class=\"btn btn-primary\" href=\"/upload_contents_detail/82/\">コンテンツの詳細</a></div>\r\n</div>\r\n</div>\r\n\r\n<div class=\"headline3\">\r\n<h2>vaundy と niziu</h2>\r\n\r\n<div class=\"contents\">\r\n<div class=\"content-item\">\r\n<audio class=\"audio-player\" controls=\"\" src=\"/media/01%20COCONUT.m4a\">&nbsp;</audio>\r\n\r\n<p class=\"audio-name\">01 COCONUT.m4a</p>\r\n<a class=\"btn btn-primary\" href=\"/upload_contents_detail/84/\">コンテンツの詳細</a></div>\r\n\r\n<div class=\"content-item\">\r\n<audio class=\"audio-player\" controls=\"\" src=\"/media/01%20%E7%9E%B3%E6%83%9A%E3%82%8C.m4a\">&nbsp;</audio>\r\n\r\n<p class=\"audio-name\">01 瞳惚れ.m4a</p>\r\n<a class=\"btn btn-primary\" href=\"/upload_contents_detail/85/\">コンテンツの詳細</a></div>\r\n</div>\r\n</div>',1,0,'2023-12-11 16:58:59.425991','2023-12-11 17:00:22.492507',0,NULL,1,NULL,1),(29,'	ヨーデル食べ放題 着信音.mp3','<div class=\"headline1\">\n    <h2>	ヨーデル食べ放題 着信音.mp3</h2>\n    <p>	ヨーデル食べ放題 着信音.mp3</p>\n    <div class=\"contents\">\n        \n            \n            \n            \n            \n                <div class=\"content-item\">\n                    <audio src=\"/media/%E3%83%A8%E3%83%BC%E3%83%86%E3%82%99%E3%83%AB%E9%A3%9F%E3%81%B8%E3%82%99%E6%94%BE%E9%A1%8C%20%E7%9D%80%E4%BF%A1%E9%9F%B3.mp3\" controls class=\"audio-player\"></audio>\n                    <p class=\"audio-name\">ヨーデル食べ放題 着信音.mp3</p>\n                    <a class=\"btn btn-primary\" href=\"/upload_contents_detail/75/\">コンテンツの詳細</a>\n                </div>\n            \n            \n        \n    </div>\n</div>\n\n',1,0,'2023-12-13 08:57:37.025720','2023-12-13 08:57:37.025772',0,NULL,1,NULL,1),(30,'テスト記事: お知らせの重要性について','<div class=\"container mt-5\">\r\n<h1>&nbsp;</h1>\r\n\r\n<div class=\"content\">\r\n<h2>お知らせの役割</h2>\r\n\r\n<p>お知らせは、ユーザーに対して重要な情報を迅速かつ効果的に伝えるための重要な手段です。例えば、システムメンテナンス、イベントのお知らせ、新機能のリリースなど、様々な情報を提供することができます。</p>\r\n\r\n<h2>効果的なお知らせの作成方法</h2>\r\n\r\n<p>効果的なお知らせを作成するためには、以下のポイントに注意する必要があります:</p>\r\n\r\n<ul>\r\n	<li><strong>明確なタイトル:</strong> お知らせの内容を一目で理解できるタイトルをつけましょう。</li>\r\n	<li><strong>具体的な内容:</strong> 必要な情報を簡潔かつ具体的に記載しましょう。</li>\r\n	<li><strong>視覚的な要素:</strong> 画像やアイコンを使用して視覚的に魅力的なお知らせを作成しましょう。</li>\r\n	<li><strong>行動喚起:</strong> ユーザーにとって次に何をすべきかを明確に伝える行動喚起を含めましょう。</li>\r\n</ul>\r\n\r\n<h2>お知らせの例</h2>\r\n\r\n<p>以下に、効果的なお知らせの例を示します:</p>\r\n\r\n<div class=\"alert alert-info\">\r\n<h4>システムメンテナンスのお知らせ</h4>\r\n\r\n<p>2024年6月1日（土）午前2時から午前4時まで、システムメンテナンスのためサービスを一時停止いたします。この間、ご利用いただけませんのでご了承ください。</p>\r\n\r\n<hr />\r\n<p>詳細については、<a href=\"#\">こちら</a>をご覧ください。</p>\r\n</div>\r\n\r\n<h2>関連画像</h2>\r\n<img alt=\"お知らせイメージ\" class=\"img-fluid\" src=\"https://via.placeholder.com/600x400\" />\r\n<h2>リンク</h2>\r\n\r\n<p>さらに詳しい情報は、<a href=\"#\">こちらのページ</a>をご覧ください。</p>\r\n</div>\r\n</div>\r\n',0,1,'2024-05-20 08:05:43.838923','2024-10-15 08:43:08.549487',0,NULL,1,NULL,1),(31,'あ','<div class=\"headline1\">\n    <h2>あ</h2>\n    <p>あ</p>\n    <div class=\"contents\">\n        \n            \n                <div class=\"content-item\">\n                    <img src=\"C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-19-49_ガラス.jpg\" alt=\"ガラス.jpg\" class=\"img-fluid\">\n                    <p class=\"image-name\">ガラス.jpg</p>\n                    <a class=\"btn btn-primary\" href=\"/upload_contents_detail/65/\" target=\"_blank\">コンテンツの詳細</a>\n            \n            \n            \n            \n            \n        \n            \n                <div class=\"content-item\">\n                    <img src=\"C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-20-16_ガラス.jpg\" alt=\"ガラス.jpg\" class=\"img-fluid\">\n                    <p class=\"image-name\">ガラス.jpg</p>\n                    <a class=\"btn btn-primary\" href=\"/upload_contents_detail/67/\" target=\"_blank\">コンテンツの詳細</a>\n            \n            \n            \n            \n            \n        \n    </div>\n</div>\n\n',0,0,'2024-07-02 07:24:46.703928','2024-10-15 08:43:08.547397',0,NULL,10,NULL,10),(32,'タグテスト','<p>てすと</p>',0,0,'2024-08-16 18:26:51.117747','2024-08-16 18:26:51.117801',0,NULL,1,NULL,1),(33,'テスト','<p>てすと</p>\r\n',0,0,'2024-08-16 18:30:54.424981','2024-08-16 18:30:54.425062',0,NULL,1,NULL,1),(35,'あ','<p>あ</p>',0,0,'2024-09-16 15:00:43.070855','2024-09-16 15:08:52.659302',0,NULL,1,NULL,1),(36,'テスト記事','<p>この記事はテストとして作成されました。</p><h3>サンプル段落</h3><p>これは段落のサンプルです。いくつかの<strong>太字テキスト</strong>や<i>斜体テキスト</i>を含めています。</p><ul><li>リストアイテム1</li><li>リストアイテム2</li><li>リストアイテム3</li></ul><p>画像のサンプル:</p><p><img src=\"sample-image-url.jpg\" alt=\"サンプル画像\"></p><p>リンクのサンプル: <a href=\"https://example.com\">こちらをクリック</a>してください。</p>',0,0,'2024-09-19 07:46:33.709890','2024-10-02 00:28:49.103624',0,NULL,1,NULL,1),(37,'テスト記事2','<p>テスト記事です</p>',1,0,'2024-10-02 00:29:11.264056','2024-10-15 08:49:50.640474',0,NULL,1,NULL,1),(38,'テスト','<p>テスト</p>',1,0,'2024-10-02 00:35:34.805813','2024-10-15 08:49:19.083053',0,NULL,1,NULL,1),(39,'しんしゅうかんの写真','<p> </p><figure class=\"image image_resized image-style-align-center\" style=\"width:54.76%;\"><img height=\"100%\" src=\"/media//001 2024-06-11 08_38_02.jpg\" style=\"aspect-ratio:100%/100%;\" width=\"100%\"/></figure>',1,1,'2024-10-02 02:43:10.182377','2024-10-16 06:23:52.578893',0,NULL,1,NULL,1),(40,'テスト','<p>テスト</p>',0,0,'2024-10-29 14:33:18.840611','2024-10-29 14:33:18.840657',0,NULL,1,NULL,1),(41,'テスト','<div class=\"headline1\">\n<h2>テスト</h2>\n<p>テストで投稿！！！</p>\n<div class=\"contents\">\n</div>\n</div>\n',0,0,'2024-10-29 14:36:35.559389','2024-10-29 14:36:35.559413',0,NULL,1,NULL,1);
/*!40000 ALTER TABLE `ArchiveViewer_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveViewer_reportcategory`
--

DROP TABLE IF EXISTS `ArchiveViewer_reportcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ArchiveViewer_reportcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `created_by_id` bigint NOT NULL,
  `deleted_by_id` bigint DEFAULT NULL,
  `updated_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveViewer_reportcategory`
--

LOCK TABLES `ArchiveViewer_reportcategory` WRITE;
/*!40000 ALTER TABLE `ArchiveViewer_reportcategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `ArchiveViewer_reportcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveViewer_reportfavorite`
--

DROP TABLE IF EXISTS `ArchiveViewer_reportfavorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ArchiveViewer_reportfavorite` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `report_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveViewer_reportfavorite`
--

LOCK TABLES `ArchiveViewer_reportfavorite` WRITE;
/*!40000 ALTER TABLE `ArchiveViewer_reportfavorite` DISABLE KEYS */;
INSERT INTO `ArchiveViewer_reportfavorite` VALUES (24,'2024-06-13 16:47:26.899442',6,1),(25,'2024-07-02 07:25:06.145918',31,10);
/*!40000 ALTER TABLE `ArchiveViewer_reportfavorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveViewer_reporthistory`
--

DROP TABLE IF EXISTS `ArchiveViewer_reporthistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ArchiveViewer_reporthistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `report_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=332 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveViewer_reporthistory`
--

LOCK TABLES `ArchiveViewer_reporthistory` WRITE;
/*!40000 ALTER TABLE `ArchiveViewer_reporthistory` DISABLE KEYS */;
INSERT INTO `ArchiveViewer_reporthistory` VALUES (207,'2024-07-02 07:24:52.263251',31,10),(208,'2024-07-02 07:25:06.172593',31,10),(322,'2024-10-16 06:02:18.384934',39,1),(323,'2024-10-16 06:03:10.628097',39,1),(324,'2024-10-16 06:03:56.823782',39,1),(325,'2024-10-16 06:22:47.187208',39,1),(326,'2024-10-16 06:23:41.668850',39,1),(327,'2024-10-16 06:23:52.612614',39,1),(328,'2024-10-16 06:25:07.332235',6,1),(329,'2024-10-18 02:08:58.361774',29,1),(330,'2024-10-29 14:33:18.894670',40,1),(331,'2024-10-29 14:36:35.587383',41,1);
/*!40000 ALTER TABLE `ArchiveViewer_reporthistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveViewer_tag`
--

DROP TABLE IF EXISTS `ArchiveViewer_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ArchiveViewer_tag` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveViewer_tag`
--

LOCK TABLES `ArchiveViewer_tag` WRITE;
/*!40000 ALTER TABLE `ArchiveViewer_tag` DISABLE KEYS */;
INSERT INTO `ArchiveViewer_tag` VALUES (1,'あ',NULL),(2,'ああ',NULL),(3,'お知らせ',NULL),(4,'テスト記事',NULL),(5,'テスト',NULL),(12,'Python',NULL),(13,'データサイエンス',NULL),(14,'現代建築',NULL),(15,'緑地',NULL),(16,'青空',NULL),(17,'コミュニティスペース',NULL),(18,'センスオブワンダー',NULL),(19,'アート',NULL),(20,'幻想的',NULL),(21,'女性',NULL),(22,'水の要素',NULL),(23,'iPhone',NULL),(25,'音楽',NULL),(27,'い',NULL),(28,'2',NULL),(29,'テスト2',NULL);
/*!40000 ALTER TABLE `ArchiveViewer_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveViewer_tag_report_models`
--

DROP TABLE IF EXISTS `ArchiveViewer_tag_report_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ArchiveViewer_tag_report_models` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_id` bigint NOT NULL,
  `report_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ArchiveViewer_tag_report_models_tag_id_report_id_3ba2cb53_uniq` (`tag_id`,`report_id`),
  KEY `ArchiveViewer_tag_re_report_id_bfeffd54_fk_ArchiveVi` (`report_id`),
  CONSTRAINT `ArchiveViewer_tag_re_report_id_bfeffd54_fk_ArchiveVi` FOREIGN KEY (`report_id`) REFERENCES `ArchiveViewer_report` (`id`),
  CONSTRAINT `ArchiveViewer_tag_re_tag_id_17f2b54a_fk_ArchiveVi` FOREIGN KEY (`tag_id`) REFERENCES `ArchiveViewer_tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveViewer_tag_report_models`
--

LOCK TABLES `ArchiveViewer_tag_report_models` WRITE;
/*!40000 ALTER TABLE `ArchiveViewer_tag_report_models` DISABLE KEYS */;
INSERT INTO `ArchiveViewer_tag_report_models` VALUES (1,1,33),(2,2,33),(8,3,30),(9,4,30),(16,5,3),(7,5,10),(17,5,12),(10,5,30),(11,23,6),(21,27,35),(23,28,37),(24,29,38);
/*!40000 ALTER TABLE `ArchiveViewer_tag_report_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveViewer_tag_upload_models`
--

DROP TABLE IF EXISTS `ArchiveViewer_tag_upload_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ArchiveViewer_tag_upload_models` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_id` bigint NOT NULL,
  `upload_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ArchiveViewer_tag_upload_models_tag_id_upload_id_d520dc33_uniq` (`tag_id`,`upload_id`),
  KEY `ArchiveViewer_tag_up_upload_id_35111c34_fk_upload_fi` (`upload_id`),
  CONSTRAINT `ArchiveViewer_tag_up_tag_id_bf9cc918_fk_ArchiveVi` FOREIGN KEY (`tag_id`) REFERENCES `ArchiveViewer_tag` (`id`),
  CONSTRAINT `ArchiveViewer_tag_up_upload_id_35111c34_fk_upload_fi` FOREIGN KEY (`upload_id`) REFERENCES `upload` (`file_id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveViewer_tag_upload_models`
--

LOCK TABLES `ArchiveViewer_tag_upload_models` WRITE;
/*!40000 ALTER TABLE `ArchiveViewer_tag_upload_models` DISABLE KEYS */;
INSERT INTO `ArchiveViewer_tag_upload_models` VALUES (6,12,95),(7,13,95),(8,14,95),(9,15,95),(10,16,95),(11,17,95),(12,18,80),(13,19,80),(14,20,80),(15,21,80),(16,22,80),(71,25,75),(69,25,85);
/*!40000 ALTER TABLE `ArchiveViewer_tag_upload_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveViewer_uploadfavorite`
--

DROP TABLE IF EXISTS `ArchiveViewer_uploadfavorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ArchiveViewer_uploadfavorite` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `upload_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveViewer_uploadfavorite`
--

LOCK TABLES `ArchiveViewer_uploadfavorite` WRITE;
/*!40000 ALTER TABLE `ArchiveViewer_uploadfavorite` DISABLE KEYS */;
INSERT INTO `ArchiveViewer_uploadfavorite` VALUES (6,'2023-10-18 10:20:37.394321',67,1),(8,'2023-11-08 14:14:31.361180',84,1),(9,'2023-11-09 04:27:12.910906',85,1),(10,'2023-11-10 16:43:13.033253',92,1),(11,'2024-08-24 07:54:45.237203',95,1);
/*!40000 ALTER TABLE `ArchiveViewer_uploadfavorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveViewer_uploadhistory`
--

DROP TABLE IF EXISTS `ArchiveViewer_uploadhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ArchiveViewer_uploadhistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `upload_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1291 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveViewer_uploadhistory`
--

LOCK TABLES `ArchiveViewer_uploadhistory` WRITE;
/*!40000 ALTER TABLE `ArchiveViewer_uploadhistory` DISABLE KEYS */;
INSERT INTO `ArchiveViewer_uploadhistory` VALUES (1193,'2024-07-02 07:24:54.990431',65,10),(1281,'2024-10-29 15:15:04.194945',102,1),(1282,'2024-10-29 15:18:01.006110',75,1),(1283,'2024-10-29 15:18:13.008205',102,1),(1284,'2024-10-29 15:19:04.270134',95,1),(1285,'2024-10-29 15:19:21.327772',92,1),(1286,'2024-10-29 15:19:32.298029',102,1),(1287,'2024-10-29 15:19:36.576912',102,1),(1288,'2024-10-29 15:46:38.456254',89,1),(1289,'2024-10-29 15:46:39.995264',87,1);
/*!40000 ALTER TABLE `ArchiveViewer_uploadhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add site',6,'add_site'),(22,'Can change site',6,'change_site'),(23,'Can delete site',6,'delete_site'),(24,'Can view site',6,'view_site'),(25,'Can add email address',7,'add_emailaddress'),(26,'Can change email address',7,'change_emailaddress'),(27,'Can delete email address',7,'delete_emailaddress'),(28,'Can view email address',7,'view_emailaddress'),(29,'Can add email confirmation',8,'add_emailconfirmation'),(30,'Can change email confirmation',8,'change_emailconfirmation'),(31,'Can delete email confirmation',8,'delete_emailconfirmation'),(32,'Can view email confirmation',8,'view_emailconfirmation'),(33,'Can add social account',9,'add_socialaccount'),(34,'Can change social account',9,'change_socialaccount'),(35,'Can delete social account',9,'delete_socialaccount'),(36,'Can view social account',9,'view_socialaccount'),(37,'Can add social application',10,'add_socialapp'),(38,'Can change social application',10,'change_socialapp'),(39,'Can delete social application',10,'delete_socialapp'),(40,'Can view social application',10,'view_socialapp'),(41,'Can add social application token',11,'add_socialtoken'),(42,'Can change social application token',11,'change_socialtoken'),(43,'Can delete social application token',11,'delete_socialtoken'),(44,'Can view social application token',11,'view_socialtoken'),(45,'Can add user',12,'add_user'),(46,'Can change user',12,'change_user'),(47,'Can delete user',12,'delete_user'),(48,'Can view user',12,'view_user'),(49,'Can add upload',13,'add_upload'),(50,'Can change upload',13,'change_upload'),(51,'Can delete upload',13,'delete_upload'),(52,'Can view upload',13,'view_upload'),(53,'Can add report',14,'add_report'),(54,'Can change report',14,'change_report'),(55,'Can delete report',14,'delete_report'),(56,'Can view report',14,'view_report'),(57,'Can add upload history',15,'add_uploadhistory'),(58,'Can change upload history',15,'change_uploadhistory'),(59,'Can delete upload history',15,'delete_uploadhistory'),(60,'Can view upload history',15,'view_uploadhistory'),(61,'Can add upload favorite',16,'add_uploadfavorite'),(62,'Can change upload favorite',16,'change_uploadfavorite'),(63,'Can delete upload favorite',16,'delete_uploadfavorite'),(64,'Can view upload favorite',16,'view_uploadfavorite'),(65,'Can add report history',17,'add_reporthistory'),(66,'Can change report history',17,'change_reporthistory'),(67,'Can delete report history',17,'delete_reporthistory'),(68,'Can view report history',17,'view_reporthistory'),(69,'Can add report favorite',18,'add_reportfavorite'),(70,'Can change report favorite',18,'change_reportfavorite'),(71,'Can delete report favorite',18,'delete_reportfavorite'),(72,'Can view report favorite',18,'view_reportfavorite'),(73,'Can add report category',19,'add_reportcategory'),(74,'Can change report category',19,'change_reportcategory'),(75,'Can delete report category',19,'delete_reportcategory'),(76,'Can view report category',19,'view_reportcategory'),(77,'Can add announcement',20,'add_announcement'),(78,'Can change announcement',20,'change_announcement'),(79,'Can delete announcement',20,'delete_announcement'),(80,'Can view announcement',20,'view_announcement'),(81,'Can add email change request',21,'add_emailchangerequest'),(82,'Can change email change request',21,'change_emailchangerequest'),(83,'Can delete email change request',21,'delete_emailchangerequest'),(84,'Can view email change request',21,'view_emailchangerequest'),(85,'Can add tag',22,'add_tag'),(86,'Can change tag',22,'change_tag'),(87,'Can delete tag',22,'delete_tag'),(88,'Can view tag',22,'view_tag');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-05-20 12:26:20.221995','3','admin1@admin.com',3,'',7,1),(2,'2024-05-20 12:26:35.787147','1','admin@admin.com',2,'[{\"changed\": {\"fields\": [\"E\\u30e1\\u30fc\\u30eb\\u30a2\\u30c9\\u30ec\\u30b9\"]}}]',12,1),(3,'2024-06-12 14:28:54.465208','94','Upload object (94)',2,'[{\"changed\": {\"fields\": [\"Title\"]}}]',13,1),(4,'2024-06-13 17:00:51.481238','3','test@test.com',1,'[{\"added\": {}}]',12,1),(5,'2024-06-13 17:01:04.593154','3','test@test.com',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',12,1),(6,'2024-06-13 17:02:58.317444','4','test@test.com',2,'[{\"changed\": {\"fields\": [\"Verified\", \"Primary\"]}}]',7,1),(7,'2024-06-14 08:17:53.456727','3','test1@test.com',3,'',12,1),(8,'2024-06-14 16:56:32.988535','1','localhost',2,'[{\"changed\": {\"fields\": [\"Domain name\", \"Display name\"]}}]',6,1),(9,'2024-06-14 16:58:43.700267','1','127.0.0.1:8000',2,'[{\"changed\": {\"fields\": [\"Domain name\", \"Display name\"]}}]',6,1),(10,'2024-06-14 17:29:56.844642','4','test@test.com',3,'',12,1),(11,'2024-06-14 17:29:56.847534','5','test1@test.com',3,'',12,1),(12,'2024-07-02 04:35:09.348037','10','test4@test.com',3,'',7,1),(13,'2024-07-02 07:21:54.937769','10','syun100000@gmail.com',2,'[{\"changed\": {\"fields\": [\"Is staff\", \"Is superuser\"]}}]',12,1),(14,'2024-08-08 07:24:06.198607','11','staff@staff.com',2,'[{\"changed\": {\"fields\": [\"Last name\", \"First name\", \"Is staff\"]}}]',12,1),(15,'2024-08-16 17:05:44.969037','1','a',1,'[{\"added\": {}}]',22,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'account','emailaddress'),(8,'account','emailconfirmation'),(21,'accounts','emailchangerequest'),(12,'accounts','user'),(1,'admin','logentry'),(20,'ArchiveViewer','announcement'),(14,'ArchiveViewer','report'),(19,'ArchiveViewer','reportcategory'),(18,'ArchiveViewer','reportfavorite'),(17,'ArchiveViewer','reporthistory'),(22,'ArchiveViewer','tag'),(13,'ArchiveViewer','upload'),(16,'ArchiveViewer','uploadfavorite'),(15,'ArchiveViewer','uploadhistory'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session'),(6,'sites','site'),(9,'socialaccount','socialaccount'),(10,'socialaccount','socialapp'),(11,'socialaccount','socialtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'accounts','0001_initial','2023-09-20 13:36:24.586424'),(2,'ArchiveViewer','0001_initial','2023-09-20 13:40:24.031530'),(3,'account','0001_initial','2023-09-20 13:40:24.098121'),(4,'account','0002_email_max_length','2023-09-20 13:40:24.106532'),(5,'contenttypes','0001_initial','2023-09-20 13:40:24.118338'),(6,'admin','0001_initial','2023-09-20 13:40:24.151624'),(7,'admin','0002_logentry_remove_auto_add','2023-09-20 13:40:24.155759'),(8,'admin','0003_logentry_add_action_flag_choices','2023-09-20 13:40:24.159449'),(9,'contenttypes','0002_remove_content_type_name','2023-09-20 13:40:24.178763'),(10,'auth','0001_initial','2023-09-20 13:40:24.249238'),(11,'auth','0002_alter_permission_name_max_length','2023-09-20 13:40:24.264305'),(12,'auth','0003_alter_user_email_max_length','2023-09-20 13:40:24.266932'),(13,'auth','0004_alter_user_username_opts','2023-09-20 13:40:24.269992'),(14,'auth','0005_alter_user_last_login_null','2023-09-20 13:40:24.273109'),(15,'auth','0006_require_contenttypes_0002','2023-09-20 13:40:24.274071'),(16,'auth','0007_alter_validators_add_error_messages','2023-09-20 13:40:24.277099'),(17,'auth','0008_alter_user_username_max_length','2023-09-20 13:40:24.279962'),(18,'auth','0009_alter_user_last_name_max_length','2023-09-20 13:40:24.282376'),(19,'auth','0010_alter_group_name_max_length','2023-09-20 13:40:24.291306'),(20,'auth','0011_update_proxy_permissions','2023-09-20 13:40:24.297792'),(21,'auth','0012_alter_user_first_name_max_length','2023-09-20 13:40:24.300368'),(22,'sessions','0001_initial','2023-09-20 13:40:24.310408'),(23,'sites','0001_initial','2023-09-20 13:40:24.315717'),(24,'sites','0002_alter_domain_unique','2023-09-20 13:40:24.321087'),(25,'socialaccount','0001_initial','2023-09-20 13:40:24.410397'),(26,'socialaccount','0002_token_max_lengths','2023-09-20 13:40:24.432838'),(27,'socialaccount','0003_extra_data_default_dict','2023-09-20 13:40:24.436441'),(28,'account','0003_alter_emailaddress_create_unique_verified_email','2024-05-20 01:17:42.708498'),(29,'account','0004_alter_emailaddress_drop_unique_email','2024-05-20 01:17:42.741093'),(30,'account','0005_emailaddress_idx_upper_email','2024-05-20 01:17:42.759538'),(31,'accounts','0002_rename_active_user_is_active_and_more','2024-05-20 01:17:42.811158'),(32,'socialaccount','0004_app_provider_id_settings','2024-05-20 01:17:42.857281'),(33,'socialaccount','0005_socialtoken_nullable_app','2024-05-20 01:17:42.894684'),(34,'ArchiveViewer','0002_announcement','2024-05-20 12:44:41.236904'),(35,'ArchiveViewer','0003_announcement_is_html_announcement_is_public','2024-06-12 16:27:52.337714'),(36,'accounts','0003_user_date_joined_user_groups_user_user_permissions_and_more','2024-06-14 08:15:51.563512'),(37,'accounts','0004_emailchangerequest','2024-06-14 17:29:25.203548'),(38,'accounts','0005_delete_emailchangerequest','2024-07-02 04:21:26.778584'),(39,'ArchiveViewer','0004_tag_alter_upload_options_report_tags','2024-08-14 02:26:21.715046'),(40,'ArchiveViewer','0005_upload_tags_alter_tag_description_and_more','2024-08-16 17:07:18.810367'),(41,'ArchiveViewer','0005_upload_tags_alter_upload_user_id','2024-08-16 17:29:44.131016'),(42,'ArchiveViewer','0004_alter_upload_options_tag','2024-08-16 18:16:06.913208'),(43,'ArchiveViewer','0005_alter_upload_user_id','2024-08-16 18:16:06.935660'),(44,'ArchiveViewer','0006_alter_announcement_options_alter_report_options_and_more','2024-10-23 07:00:23.074888');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('082aozmrwvyv48rmzb3pgusps2i2xum1','.eJxVjssOgyAQRf-FdUN4CeKu_RGCwxBJDTaCSZum_140LtrlfcyZ-ybOb3VyW8HVpUAGwsnl1xs93DHvgZ_n3aYeYNlypUfnjAu9NoW5JvA1Lfl2Xv2hJl-mxpFc94AxRq6UFVoKrQNyIfXILLDITBMGRwgaPQRUPWMcI4MujCbEDhr0nHCwz6cYnK9k4EYoyZW0khrZW6Ztm1CwlDbK4fOR1hcZ2OcLSuFScw:1sh2wT:_dU8GYU4ndAb8wtxTaMfNd4JS9PTK1rqmo5eOpCjhB8','2024-09-05 08:13:13.740542'),('0t8w0ksqd9z5wdv3xqxj2c8t0f6tc0n6','.eJxVjk0OgyAQhe_CujEDIoi79iIEhiGSGm0EkzZN7140Ltrl-5lv3ptZt5XRbplWmwIbGGeXX887vNO8B26adrtxiMs2l-bonHFurlXRXBK6kpb5dl79oUaXx8ppueqRYoxcSiNUK5QKxEWrPBiECLoKTR6DIoeBZA_AKQJ2wesQO6zQc8LBPp9SsK6wgesWhBLGdI0GkF1fF2TKuW6y9Hyk9cUG-HwB-0xSOA:1t60Rf:s-4xcNnClveCoXipPk8XFLfses2tGSGC3b1saGWlHFE','2024-11-13 04:36:35.702113'),('1fbpdbm9nirx7icim9mf8cgr6rygqfie','.eJxVjsFuwyAQRP-Fc4S8NhjsY-_5BrQsS0xbQWSw1CrKv9eufEiuM2-e5iEcbm1xW-XVpSBmAeLymnmkL85HET4x34qkktuavDwQebZVXkvg74-TfRMsWJd97ZW1QGyA4qAVaGNtVAPASDyqDgYfRooqaq0nFTqCDsYdRkZAP8VIuxSJypbbv5tzS4SNg8MmZjBge-h7Y6XSRpt-f1C51lSy4597Wn_F3D3_ALqFTQg:1sHRVG:VPDPGslfIVv9cLz-H4L9h3hQPMNj5m-2hFGPW4vIXLw','2024-06-26 17:11:18.459036'),('2yddzph853ndh0hcto6l0pc8uqg31itd','.eJxVjssOgyAQRf-FdWN4Cequ_RECwxBJDTaCSZum_140LNrlfcyZ-ybG7mU2e8bNRE8mwsjl13MW7piOwC7LYXcWYN1T6c5Oi3N3rQpTiWBLXNOtXf2hZpvnyhFMDYAhBCblyJXgSnlkXChHR6CB6io0OvAKLXiUA6UMA4XeO-1DDxXaJpzs9hS9sYVMTHMpGOdCd7LnWum6IGPOdZPB5yNuLzLRzxf6ilIz:1sh2Nh:jfGGiLi6MVDWl_XZqh_qYxpAmqO3rPpClkjA8SoDU04','2024-09-05 07:37:17.456083'),('32bf0b7zhudusu0mbcn0o76r9iuur48w','.eJxVjssOgjAQRf-la0P6nAI7_ZGmTKehkYChJdEY_91CWOjyPubMfTPntzK6LdPqUmA9E-zy6w0e7zTvgZ-m3W484rLNpTk6Z5yba1U0l4S-pGW-nVd_qNHnsXKUgBYpxii07iQoCRBISAUD75BHbquwNGAA8hhIt5wLihxNGGyIBiv0nHCwz6cUnC-sF1baVhkA1egOlDF1Qaac6yZHz0daX6znny_8ylJE:1svoz9:suZinmquw4XHmGPMSCy8P7HJC_8oWhFqYgaFMJfn7FI','2024-10-16 02:21:03.497915'),('4ezcqcbos7ye75ryw6afcnqeusun1cgq','.eJxVjk0OgyAQhe_CujGDCKi79iIEhiGSGm0EkzZN7140LNrl-5lv3psZu-fJ7Ik2Ez0bGWeXX89ZvNNyBHaeD7uxiOu-5Obs1Dg116JoyRFtjutyq1d_qMmmqXAEVz1SCIF33dAq0SrlibdCORgQAugiNDn0iix66noATgFQeqd9kFigdcLJrk_JG5vZyLWAtsD6oZFKCJBlQaKUyiZDz0fcXmyEzxf6J1Iu:1t5nHR:kyQbR9HsWdxKSWPfKJQsh7fMPpHgw0jO0IN6AAIZJx8','2024-11-12 14:33:09.565475'),('66eo40dnm1x7jm2lnvmwt6c5m8ajkffp','.eJxVjkuOwjAQRO_iNbLS8idOluw5g9Vut4kB2Sh2JNBo7j5hxAK2Va-e6kd43Prit8arz1HMAsThMwtIVy6vIl6wnKukWvqag3wh8t02eaqRb8c3-yVYsC37OmjngHgESspoMKNzSSsAS2z1ACpES0knY8yk40AwgN1hZAQMU0q0S5GobqX_u7n0TNg5euxihhGcMqCmSVrQ1tn9QePWci2eH_e8PsU8_P4Bu41NEQ:1sI1h9:URhpyKqmo4okmNDlyMnsdIbSCoL7r_gJPjfcnTDEQxY','2024-06-28 07:49:59.615703'),('7fwfcfhqy4ncbv1z2zmx640zw4xb6nb8','.eJxVjs0KwyAQhN_Fcwn-JBpza19EdF2JNJgSDbSUvntN8NAeZ2bn23kTY_cymz3jZqInE2Hk8us5C3dMR2CX5bA7C7DuqXTnTYtzd60KU4lgS1zTrbX-ULPNc-UIJkfAEALre82l4FJ6ZFxIRzXQQFUVCh14iRY89iOlDAOFwTvlwwAV2iac7PYUvbGFTExxLWqDs05TzcVQF2TMuW4y-HzE7UUm-vkC-qFSMQ:1t2Ik9:y0FhWEeL7o39FN8ogGD1bhjb0CePY23WHw3tajj1I1o','2024-11-02 23:20:21.910621'),('9g697tahsxn3760waakcuraerwr90bwi','.eJxVjstuwyAURP-FdYUM2Bi87L7fgK7vo6atoDJYSlT13-tUWSTbOTNH86MSHH1LR-M9ZVKLMurlMVsBP7ncAH1Aea8aa-l7XvWtou-06bdK_PV67z4JNmjbubZr9I4NoeUwr2IGLzKSOMtoaHIkIBQijKOnQOg8iZjohNEFM1iaTykg1qP0fzeXnhE6U4KuFuNjNDGMYdKzi3YK4bzQuLVcS-LLd96vahl-_wCaJU6M:1qzf9B:Tysp4M9RL2mufbyLDJgjdUF977nZ1xqOSbtiR2uZfB8','2023-11-19 15:34:45.740727'),('9pkyx9mrhibn384gxyhv7i0bz4uy56qz','.eJxVjstOwzAURP_Fa2T5kThOluz5BuvmPogB2Sh2pFaIfydFXbTbOTNH86MSHH1LR-M9ZVKLsurlMVsBP7ncAH1Aea8aa-l7XvWtou-06bdK_PV67z4JNmjbuXbrHDxbQsdxWsWaIDKQeMdoafQkIBRnGIZAkdAHErGzF0YfrXE0nVJArEfp_24uPSN0pgRdLXYyLozBuFmbOHk_xvNC49ZyLYkv33m_qsX8_gGWWE5u:1rEAc1:-ejq1vnc5e2XE1YJUXyxI4YyxP67H8IetTwi-NwlCaM','2023-12-29 16:00:29.089937'),('9y7m62nmfv1q7h4wnc0mka44xwzwawfb','.eJxVjklOxTAQRO_iNbLSHjIt2XMGq9MDMSAbxY4EQtydfPQXsK1X9VRfJuHZ93Q2OVJmsxowD3-zDelVyg3wC5bnaqmWfuTN3ir2Tpt9qixvj_fuP8GObb_WbltGL8DkZJ42hWFUDazeCQFHz4rK84IhjDwz-ZFVYfEq5GcYHE-XFInqWfqvW0rPhF04YTcrTBBD9BGidXEK3l0PmrSWa0ny8Z6PT7MO3z9KvE4y:1s5rp5:mBYg3PzBqicx838spr213ggB3i79-Zwz6XHG4WaVtFc','2024-05-25 18:51:55.260149'),('an3kweuokdf3df4mg178kd0ldfv1e323','.eJxVjk0OwiAQhe_C2jRAKZTu9CIEhiElNtQUmmiMd5c2LHT5fuab9ybG7mU2e8bNRE8mwsjl13MW7piOwC7LYXcWYN1T6c5Oi3N3rQpTiWBLXNOtXf2hZpvnyumZHAFDCEwIzWXPpfTIeC8d1UADVVUodOAlWvAoRkoZBgqDd8qHASq0TTjZ7Sl6YwuZmOJSaMUV77SiUox1Qcac6yaDz0fcXmSiny_82lJF:1sqCoC:fJkk1OZe6VtlQep3McEvKMU4BKh5h5nRvnDBldus9h8','2024-09-30 14:34:32.972712'),('b3az9k03al2wdre72hhhihlmi7oqa8lk','.eJxVjMEOwiAQBf-FsyEFKoUevfsNBNhdQQ00pU00xn_XJj3o9c28eTHn1yW5teHsMrCRCXb43YKPNywbgKsvl8pjLcucA98UvtPGzxXwftrdv0DyLX3fMlitUECUaIZAotNEPZCSGAUcFZAnMNb3vQYDUWkgElYRRmVEJ2HYog1by7U4fEx5frKxe38Ay1VAOw:1qt6eT:trg7Dl0WTc6FrpnoDiZt8eOIEq9uNt9QznbV-bxhKb8','2023-11-01 13:31:57.082088'),('cvv59tgndxhfdkjjzi7lb3hm938s3q8p','.eJxVjk0OgyAQhe_CuiGAOKi79iIEhiGaGmwEkzZN7140Ltrl-5lv3ptZt5XRbplWOwU2MMkuv553eKe0B26ed5s7xGVLhR-dM878WhWlMqEr05Ju59UfanR5rJxGQocUY5Ra9woaBRBIqga86FFEYaow5DEAOQykOyEkRYFt8CbEFiv0nHCwz6cUrCtskEb1AGAAOGgltaoLMuVcN1l6Pqb1xQbx-QL8jFI_:1t3VL4:q5ck8tiv7EUby1nUe445mqr4vQpey-7caG5ww-BNi1o','2024-11-06 06:59:26.644168'),('dc63mscy1gbacnz2plbu62nquxsbedn1','.eJxVjklOxDAURO_iNbI8pB07S_acwfr5AzEgG8WOBGr13UmjXsC2XtVTXVWGY2z56LznQmpRVj39zVbAd653QG9QX5vGVsdeVn2v6Aft-qURfzw_uv8EG_TtXLs1Bc-W0HGcV7EmiEwk3jFaungSEIoJpilQJPSBRGzywuijNY7mUwqI7ajj1811FITBlGGoxc7GmORd8tqGOJnL-aBz76XVzF-fZf9Wi7n9AEpTTjA:1r3PvZ:cWCvx48uBiIlhqORtZvbY82LtZdzU3bxkcrC8NlHBd4','2023-11-30 00:08:13.170030'),('ea235klh8zx3lpn4w645k0utbnlmep1w','.eJxVjssOgyAQRf-FdWMAeemu_RECwxBJjTaCSZum_140LNrlfcyZ-ybW7WWye8bNpkBGwsjl1_MO7rgcgZvnw-4cwLovpTs7Lc7dtSpcSgJX0rrc2tUfanJ5qpyeKQMYY2RCDFz1XKmAjPfK0wFopLoKjR6CQgcBhaGUYaQgg9chSqjQNuFkt6cYrCtkZJoLPRhpZNdLxpQwdULGnOsoi89H2l5kpJ8vS_JSeA:1sj4u1:BlgZSWOvAf_JHOivoTOUzgjxIQuQmPVHkhkyHvyuP6s','2024-09-10 22:43:05.352515'),('gf9urp9bzq2y81znjc8j1mubglrreblg','.eJxVjs1uwyAQhN-Fc4VY8WPsY-95BrQsS01bQWSwlCjKu8eJcmivM998mpsIuI817J23UJJYBIiPv1lE-uH6LNI31q8mqdWxlSifiHy3XZ5a4t_PN_tPsGJfj3U03gPxBJS1NWAn77PRAI7YGQU6JkfZZGvtbJIiUOAOGBkB45wzHVIkansdLzfXUQgHp4BDLDCB024yXks9e-XheNC599Jq4Mu5bFexqPsDu2BNDg:1s9haV:6WknZPX92kRxeKmC32oia59v8rabfuXmh6axg3T9lVw','2024-06-05 08:44:43.399478'),('i2tzf7z6x5ijbnod29cf6cs6g0sw18vx','.eJxVjMEOwiAQBf-FsyEFKoUevfsNBNhdQQ00pU00xn_XJj3o9c28eTHn1yW5teHsMrCRCXb43YKPNywbgKsvl8pjLcucA98UvtPGzxXwftrdv0DyLX3fMlitUECUaIZAotNEPZCSGAUcFZAnMNb3vQYDUWkgElYRRmVEJ2HYog1by7U4fEx5frKxe38Ay1VAOw:1qqjVT:Vx9LMZOqZ85SC15qyJk1LXjdM2aVYWWk6fRMUydhCV4','2023-10-26 00:24:51.309287'),('j4zgey5hlzfa1w64jlqvembzlg359qia','.eJxVjstqwzAURP9F6yD0cGTZy-77DeL6PmK1RSqWDC0h_16nZJFs58wc5qoS7H1Ne-MtZVKzsur0nC2An1zugD6gXKrGWvqWF32v6Adt-r0Sf709ui-CFdp6rN0yBc-W0HEcF7EmiAwk3jFaOnsSEIoTDEOgSOgDidjJC6OP1jgaDykg1r30fzeXnhE6U4KuZjsaO5nxHAYdvfMmHg8at5ZrSfzznbdfNZvbH0siTjY:1rB1u0:q-NAI6pNrz1r59pTdYLUeZERCTMRHrAp7_KJLFek_Hw','2023-12-21 00:06:04.835750'),('khuznhzqxsm2ekqt9dg433xe2ea4qbo1','.eJxVjsFuwyAQRP-Fc4VY4wL2sfd8A1qzuzVtBZHBUqKo_16nyiG5zpt5mpuKuPc17o23mEnNCtTbc7Zg-uZyB_SF5bPqVEvf8qLvFf2gTZ8q8c_Ho_siWLGtx3pYJmcZKA0c_CJgnMhIYgdOQO-WBIXChOPoKFCyjkRgssLJBjAD-UOKKdW99H83l54TdqaIXc3gDXgPowXtHYAJx4PGreVaIl_Oebuq2fz-AUofTi0:1rASUJ:04rji7t_zZ47ox4FkNFQtPaeQ3Qh3AyN-0DpC2Op9-c','2023-12-19 10:17:11.763679'),('kskchs7jg88hj9qke2y4as6tdb74kyyt','.eJxVjk0OgyAQhe_CujGDIKi79iIEhyGSGmwEkzZN7140LNrl-5lv3psZu-fZ7Ik2ExwbGWeXX2-yeKd4BHZZDruxiOsec3N2apyaa1EUc0Cbwxpv9eoPNds0F47gqkfy3nMph1aJVilHvBVqggHBgy5C04ROkUVHsgfg5AE7N2nnOyzQOuFk16fkjM1s5LqVosC4bAB03yleJiRKqYwy9HyE7cVG-HwBSEVSWw:1sh2Ow:nSlNdpx3Yme41pivikUPOeVCW46nPa7EfMMU44idDHI','2024-09-05 07:38:34.010023'),('ldnvc9eatfxwnmk1jymbtnisrao4aekm','.eJxVjssOgyAQRf-FdWN4Cequ_RECwxBJDTaCSZum_140LNrlfcyZ-ybG7mU2e8bNRE8mwsjl13MW7piOwC7LYXcWYN1T6c5Oi3N3rQpTiWBLXNOtXf2hZpvnyhFMDYAhBCblyJXgSnlkXChHR6CB6io0OvAKLXiUA6UMA4XeO-1DDxXaJpzs9hS9sYVMTHOlBRsE74SSQoq6IGPOdZPB5yNuLzLRzxf67lIz:1srBpQ:Y2eZkQSmxkUiHYdrOHax4wXr4d463KnO9dvHuB3FYqQ','2024-10-03 07:43:52.367646'),('m21botnsor1ch8vxu4q9ws5yiqday3vz','.eJxVjMEOgyAQRP-Fc2NcFgR6qz9ClmUbTQ0mFU5N_73aeGiP82bmvVSkVqfYNnnGOaurgl5dfmEifkg5GlqWA3fEvLZSu-_mrLfuticpdWaq81rG8_Wnmmibdk8WHJz3FhiDR9R3m4IwBzA56QxeqAfwhrXBAINBB4GzZu28WIZE6v0Bx9M76Q:1sOXq0:FTarcy7mclsj6_DOim1ymZ_DLt1s1JQ7rPPIXG_voFQ','2024-07-16 07:22:04.653973'),('mmdwv4giceqz91xxrgqvhj86ppdk5bx4','.eJxVjssOgjAQRf-la9Mw9kFhpz_STKfTQCRgbEk0xn-3EBa6nPs4c9_C41oGv2Z--DGKXoA4_WoB6cbzZuA0bbJEomWdi9wzh53lpV48l5GwjMt8PVp_qAHzUDlBOwfELVBSRoNpnUtaAVhiqxtQIVpKOhljOh0bggZsDSMjYOhSogo9Juzs4ylHj0X00IJTzlilpbMG9LkuyJxz3eT5eR8fL9E3ny-0rFF_:1sIAbK:7kOiSGgZUnPQpTeikQVpuf-VBxQNmWtYl9sK9Kgtw7k','2024-06-28 17:20:34.866672'),('n0n66pgpmim3gwxkgnd4xzpetjgvtttr','.eJxVjstOwzAURP_Fa2T5kThOluz5BuvmPogB2Sh2pFaIfydFXbTbOTNH86MSHH1LR-M9ZVKLsurlMVsBP7ncAH1Aea8aa-l7XvWtou-06bdK_PV67z4JNmjbuXbrHDxbQsdxWsWaIDKQeMdoafQkIBRnGIZAkdAHErGzF0YfrXE0nVJArEfp_24uPSN0pgRdLXYybjbRDKMebfDGnw8at5ZrSXz5zvtVLeb3D0ocTiw:1rFEAn:tvRYfoZlnyKGf708i0PWF75Kfiwl5KhAFpTJIv4y0pE','2024-01-01 14:00:45.519063'),('nm7h2e99l2js4p9ir3zoh15u8dgg9ha3','.eJxVjs1OxiAURN-FtSG90BbapXufgdzeH4saMIUmGuO72898C93OmTmZL5Pw7Hs6mxwps1kNmIe_2Yb0KuUG-AXLc7VUSz_yZm8Ve6fNPlWWt8d7959gx7Zfa7ctsxdgchLDpjDMqiOrd0LAk2dF5bjgOM4cmfzMqrB4FfIRBsfhkiJRPUv_dUvpmbALJ-xmhTC4cQphidYBTOE60KS1XEuSj_d8fJp1-P4BARBOCA:1rDL2k:gjfUKLS4bysXv6xj_MFtok84MX_J3iLwBAgYFXjODBU','2023-12-27 08:56:38.214726'),('oujjbcp76uqgxicxissp3nrq9z6qql5q','.eJxVjMEOwiAQBf-FsyEFKoUevfsNBNhdQQ00pU00xn_XJj3o9c28eTHn1yW5teHsMrCRCXb43YKPNywbgKsvl8pjLcucA98UvtPGzxXwftrdv0DyLX3fMlitUECUaIZAotNEPZCSGAUcFZAnMNb3vQYDUWkgElYRRmVEJ2HYog1by7U4fEx5frKxe38Ay1VAOw:1qti2c:bqQY1b6XItiJgW8rmxC_mDaI4JjlekE7YJVx8BmKUgA','2023-11-03 05:27:22.396787'),('ovuru2n6ukfr0dc00ix88nxnrafvagj2','.eJxVjssOgyAQRf-FdUN4Cequ_RECwxBNDTaCSZum_140LNrlfcyZ-ybW7WWye8bNzoGMhJPLr-cd3DEdgVuWw6YOYN1ToWenxZleq8JUZnBlXtOtXf2hJpenypFc94AxRq7UILQUWgfkQmrPBmCRmSoMeggaHQRUPWMcI4MueBNiBxXaJpzs9hSDdYWM3IheGsUGSYXishvqgow5100Wn495e5GRfb77alI4:1sy53V:5vGgKpBmJxc8ZLN2KuQJ21IR14A1UY71Eech4URqAiI','2024-10-22 07:54:53.243903'),('pym5m3e523550i9i10ewqfakwnzxbku9','.eJxVj82OwjAMhN8lZ1Q5Lvlpb-yLRG7iqhEhoCZdgVb77htQtYijvxmPxz-CvL9uubpvXuMcOTi-UExizFtKh391K7yKUXhxEI62uryAi6Ex-ckm8mfOT4FSeuJuz-henl0u3alNnGv0VOM1f-1bH1ELlaXlGBVA98deD5OC4IEwoDRAYTJKz_MAjUrjpfIKjoalt6gshgkRmYyx4v0GvY-2T6mKURrsJUiLulNDD2Bbg8KltE6O77e4PpoHYdAAv3-xDGOY:1sbxUw:VEITgXH-obqPQZRePl2N9PiYpalDrWabFJKQqy-zmoI','2024-08-22 07:23:46.594476'),('sgre83zn9wr0fra2o63bdwepttf59h80','.eJxVjEEOwiAQRe8ya0MKVEq7dO8ZCDAzFjXQlDbRGO-uTbrp9r_3_gdcpVpTyY5eU5rfMDQncH5dRrdWml1CGEDCYQs-PihvAO8-34qIJS9zCmJTxE6ruBak52V3Dwejr-O_VqE3miRGRbYLLBvD3CJrRVHiWSN7Rtv7tjVoMWqDzLLXTFFb2Sjs4PsDNhJAOw:1qixXX:TylriZS-cFD5whC7yOLBcBtQYXUR3xcLWtnLOB2axzg','2023-10-04 13:46:51.923657'),('v9wl2q8m9ul55zqipg625mhh2dnzi6vt','.eJxVjklOxDAURO_iNbLiAcfOkj1nsH7-QAzIbsWORKvF3UmjXsC2XtVT3VSGY2z56LznQmpRRj39zVbAD653QO9Q35rGVsdeVn2v6Aft-rURf748uv8EG_TtXNs1BceG0HKcVzFTEPEkzjIaenYkIBQTeB8oErpAIiY5YXTRTJbmUwqI7ajj1811FITBlGGoxYSUvI1zDDpO3jt7Pujce2k189el7Fe1TN8_TYJORw:1r0d3i:byips0YFx9CGmvhJdvnNPKbhGYzqDORY2ywNyvETFyU','2023-11-22 07:33:06.806796'),('vd6hw2e02umeuhd6i9o752n0ccerxxfm','.eJxVjssOgjAQRf-la0MY-oSd_kgzTKeBSMDQkmiM_24hLHQ593HmvoXHLQ9-S7z6MYhOgLj8aj3SnefdwGna5QqJlm3O1ZE57VRdy8VzHgnzuMy3s_WHGjANhdMr54DYAkWpFWjrXFQSwBAbVYPsg6Goota6VaEmqMGUMDIC9m2MVKDnhIN9PuXgMYsOLDjpTKNMZRtopC0LEqdUNnl-Psb1Jbr68wW0MFF7:1sIAlC:b_cr5q59Xhq5Hlv4BLbw8hP_eGN4NfO8h3yrURL_Moc','2024-06-28 17:30:46.722314'),('xgal1o7cw2dbwgxwvcqjfwoc1dyg0hfa','.eJxVjjtOxTAURPfiGln-xImdkp41WDf3QwzIRrEjgRB7Jw-9Ato5M0fzpTKcY89n5yMXUquy6uFvtgG-cr0BeoH63DS2Oo6y6VtF32nXT4347fHe_SfYoe_X2m1p9mwJHcdlE2tmkYnEO0ZLwZOAUEwwTTNFQj-TiE1eGH20xtFySQGxnXX8urmOgjCYMgy12sVOIZoQjE5LcMlfDzr3XlrN_PFejk-1mu8fS9ROPQ:1s2Cj0:lmlSa3y8KA0YrZgrhHqlFoodjYGY68-VsmAW6XgthBs','2024-05-15 16:22:30.978186'),('xvfi9b7b5e7mfk8gv5htpp56zknq8fdi','.eJxVjstqwzAURP9F6yCsR2TLy-77DeL6PmK1RSqWDC0h_16nZJFs58wc5qoS7H1Ne-MtZVKzMur0nC2An1zugD6gXKrGWvqWF32v6Adt-r0Sf709ui-CFdp6rO0Sg2NDaHkaFzFDEPEkzjIaOjsSEJoieB9oInSBREx0wugmM1gaDykg1r30fzeXnhE6U4KuZhNiHEd_Dk5H44M9DjRuLdeS-Oc7b79qHm5_AuNOFQ:1r250l:X9Ql4zVTM-maPrTnNMXrmUFDaDs06DF6ErHQYABeNDc','2023-11-26 07:36:03.916800'),('zgorpwa9wxapl5t2vzqsvitds01b49uj','.eJxVjk0OgyAQhe_CujEDKoi79iIEhiGSGm0EkzZN7140LNrl-5lv3psZu-fJ7Ik2Ez0bGWeXX89ZvNNyBHaeD7uxiOu-5Obs1Dg116JoyRFtjutyq1d_qMmmqXBaLgekEALvOi1kK6T0xEUrHWiEAKoIRQ69JIueugGAUwDsvVM-9FigdcLJrk_JG5vZyJXQIKXqRaOhB92KMiFRSmWUoecjbi82wucLSq9SbQ:1t0zFQ:nj1j6haLqHM5aIaX4tZoA883w3EygBIsw8kraBevVcQ','2024-10-30 08:19:12.906146');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'127.0.0.1:8000','127.0.0.1:8000');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `uid` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_id` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `secret` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `key` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `provider_id` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `settings` json NOT NULL DEFAULT (_utf8mb3'{}'),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `socialapp_id` int NOT NULL,
  `site_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `token_secret` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int NOT NULL,
  `app_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `upload`
--

DROP TABLE IF EXISTS `upload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `upload` (
  `file_id` int NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `insert_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `delete_flag` int NOT NULL DEFAULT '0',
  `user_id` int NOT NULL,
  `published` int NOT NULL DEFAULT '0',
  `is_unedited` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`file_id`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `upload`
--

LOCK TABLES `upload` WRITE;
/*!40000 ALTER TABLE `upload` DISABLE KEYS */;
INSERT INTO `upload` VALUES (64,'(none)','アドバイス.jpg','C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-19-42_アドバイス.jpg','(none)','2023-06-08 11:19:42','2023-10-18 14:46:20',0,4,1,1),(65,'(none)','ガラス.jpg','C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-19-49_ガラス.jpg','(none)','2023-06-08 11:19:49','2023-10-18 14:46:20',0,4,1,1),(66,'(none)','ギャグ.jpg','C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-20-02_ギャグ.jpg','as  jiok.','2023-06-08 11:20:02','2023-10-18 14:46:20',0,4,1,1),(67,'(none)','ガラス.jpg','C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-20-16_ガラス.jpg','(none)','2023-06-08 11:20:16','2023-10-18 14:46:20',0,26,1,1),(68,'(none)','スピード.jpg','C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-20-27_スピード.jpg','ui okj.','2023-06-08 11:20:27','2023-10-18 14:46:20',0,26,1,1),(69,'(none)','トキポナ.jpg','C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-20-38_トキポナ.jpg','(none)','2023-06-08 11:20:38','2023-10-18 14:46:20',0,26,1,1),(70,'(none)','トキポナ.jpg','C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-20-54_トキポナ.jpg','(none)','2023-06-08 11:20:54','2024-06-13 16:29:39',0,27,0,1),(71,'(none)','活発.jpg','C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-21-32_活発.jpg','She is very energetic girl!','2023-06-08 11:21:32','2023-10-18 14:46:20',0,27,1,1),(72,'(none)','宿泊.jpg','C:\\xampp\\htdocs\\Archive\\data/2023-06-08-11-23-17_宿泊.jpg','迷彩テントを万能スーツケースから生成し、宿泊する主人公ケイルくんの寝顔。','2023-06-08 11:23:17','2023-10-18 14:46:20',0,27,1,1),(73,'(none)','邂逅.jpg','C:\\xampp\\htdocs\\Archive\\data/2023-06-08-12-53-26_邂逅.jpg','(none)','2023-06-08 12:53:26','2023-10-18 14:46:20',0,4,1,1),(74,'てすと','【LCA概論(04)121I095斎藤隼佑.pdf','/media/%E3%80%90LCA%E6%A6%82%E8%AB%96(04)121I095%E6%96%8E%E8%97%A4%E9%9A%BC%E4%BD%91.pdf',NULL,'2023-10-19 01:35:10','2023-10-19 01:35:10',0,0,1,1),(75,'ヨーデル食べ放題 着信音.mp3','ヨーデル食べ放題 着信音.mp3','/media/%E3%83%A8%E3%83%BC%E3%83%86%E3%82%99%E3%83%AB%E9%A3%9F%E3%81%B8%E3%82%99%E6%94%BE%E9%A1%8C%20%E7%9D%80%E4%BF%A1%E9%9F%B3.mp3','ヨーデル食べ放題 着信音.mp3','2023-10-19 02:02:42','2024-08-26 16:26:48',0,0,1,1),(76,'アルバムアート','新規ファイル..jpg','/media/%E6%96%B0%E8%A6%8F%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB..jpg','サウシードッグ','2023-10-19 02:11:32','2024-08-23 19:07:45',0,0,1,1),(77,'情報アーキテクチャ','情報アーキテクチャ2021年度第14回_総括.pptx','/media/%E6%83%85%E5%A0%B1%E3%82%A2%E3%83%BC%E3%82%AD%E3%83%86%E3%82%AF%E3%83%81%E3%83%A32021%E5%B9%B4%E5%BA%A6%E7%AC%AC14%E5%9B%9E_%E7%B7%8F%E6%8B%AC.pptx',NULL,'2023-10-19 02:29:25','2023-10-19 02:29:25',0,0,1,1),(78,'アーキテクチャ','情報アーキテクチャ2021年度第14回_総括.pdf','/media/%E6%83%85%E5%A0%B1%E3%82%A2%E3%83%BC%E3%82%AD%E3%83%86%E3%82%AF%E3%83%81%E3%83%A32021%E5%B9%B4%E5%BA%A6%E7%AC%AC14%E5%9B%9E_%E7%B7%8F%E6%8B%AC.pdf',NULL,'2023-10-19 02:30:18','2023-10-19 02:30:18',0,0,1,1),(80,'ハルカミライ　','71rVyzIuu+L._UF1000,1000_QL80__lr7S9tJ.jpg','/media/71rVyzIuu%2BL._UF1000%2C1000_QL80__lr7S9tJ.jpg','画像には、女性の横顔が描かれており、彼女の髪が流れる水のように描写されています。背景は淡い青色や紫色で、泡のような円がいくつか描かれています。上部には「センスオブワンダー」と「ハルカミライ」というテキストがあります。全体的に幻想的な雰囲気が漂っています。','2023-10-20 05:12:54','2024-08-23 18:58:34',0,0,1,1),(81,'わがままジュリエット','1-07 わがままジュリエット.mp3','/media/1-07%20%E3%82%8F%E3%81%8B%E3%82%99%E3%81%BE%E3%81%BE%E3%82%B7%E3%82%99%E3%83%A5%E3%83%AA%E3%82%A8%E3%83%83%E3%83%88.mp3','','2023-11-08 13:50:19','2023-11-08 14:05:22',1,0,1,1),(82,'わがままジュリエット','1-07 わがままジュリエット.mp3','/media/1-07%20%E3%82%8F%E3%81%8B%E3%82%99%E3%81%BE%E3%81%BE%E3%82%B7%E3%82%99%E3%83%A5%E3%83%AA%E3%82%A8%E3%83%83%E3%83%88.mp3','','2023-11-08 14:05:45','2023-11-08 14:05:45',0,0,1,1),(83,'ano ','1-01 ちゅ、多様性。.flac','/media/1-01%20%E3%81%A1%E3%82%85%E3%80%81%E5%A4%9A%E6%A7%98%E6%80%A7%E3%80%82.flac','flax','2023-11-08 14:10:11','2023-11-08 14:10:11',0,0,1,1),(84,'NiziU','01 COCONUT.m4a','/media/01%20COCONUT.m4a','','2023-11-08 14:12:57','2023-11-08 14:12:57',0,0,1,1),(85,'vaundy 瞳惚れ ','01 瞳惚れ.m4a','/media/01%20%E7%9E%B3%E6%83%9A%E3%82%8C.m4a','さりげなく時は\r\nあの日まで流れ、着いた\r\n鈍い足取りは\r\n甘い香りに誘われて\r\n\r\n突き刺す音で体が揺れる\r\n予感がした\r\nまるで出会うことを知ってたかのように\r\n\r\n今虜になっていく\r\nそれはトキメクパッションで\r\n滑り込んで、瞳奪っていく\r\nほらまだ眩しいよ\r\nあれ、虜になっていく\r\nあの魅惑のパッションに\r\n滑り込んできた小悪魔も\r\nほら、踊り出して\r\nもう\r\n\r\nそれは、目まぐるしく笑い\r\n目を塞いでも、また思い出すように\r\n眩暈がするほど強い光\r\n言葉足らずの\r\nそれは瞳惚れ\r\n\r\nあの日から時は\r\n重くなり止まり出した\r\n迷う秒針はあの日の魔法に惑わされ\r\n\r\nきっと\r\n心がもたないね\r\n煮詰まり思いが噴き出て\r\nしまいそうなほど\r\n\r\n見間違いじゃないね\r\n迷う秒針が焦って\r\n巻き戻り出す前に\r\n\r\n背けるたびに体が揺れる\r\n予感がした\r\nそれは逃げることを知ってたかのように\r\n\r\nまた虜になっていく\r\nそれはトキメクパッションで\r\n滑り込んで、瞳奪っていく\r\nほらまだ眩しいよ\r\nあれ、虜になっていく\r\nあの魅惑のパッションに\r\n滑り込んできた小悪魔も\r\nほら、踊り出して\r\nもう\r\n\r\nその瞳放つ、風邪で体が痺れる\r\n予感がした\r\n振り返れば時が進んでく\r\n\r\n落ちるように\r\n\r\n今虜になっていく\r\nそれはトキメクパッションで\r\n滑り込んで、瞳奪っていく\r\nほらまだ眩しいよ\r\nあれ、虜になっていく\r\nあの魅惑のパッションに\r\n滑り込んできた小悪魔も\r\nほら、踊り出して\r\nもう\r\n\r\nそれは、目まぐるしく笑い\r\n目を塞いでも、また思い出すように\r\n眩暈がするほど強い光\r\n言葉足らずの\r\nそれは瞳惚れ','2023-11-08 14:17:27','2024-08-26 16:25:24',0,0,1,1),(86,'   0:06 / 20:11   【GOD】Lエヴァを救いたいｗｗ','watch?v=3c-zz81QtKI','https://www.youtube.com/watch?v=3c-zz81QtKI','\r\n\r\n\r\n0:06 / 20:11\r\n\r\n\r\n【GOD】Lエヴァを救いたいｗｗ','2023-11-09 05:46:01','2024-10-29 15:46:04',0,0,1,1),(87,'【GOD】Lエヴァを救いたいｗｗ','3c-zz81QtKI?si=quwvf_kd0go9tbBl','https://www.youtube.com/embed/3c-zz81QtKI?si=quwvf_kd0go9tbBl','','2023-11-09 05:48:44','2024-10-29 15:45:36',0,0,1,1),(88,'https://www.youtube.com/watch?v=3c-zz81QtKI','YouTube','https://www.youtube.com/watch?v=3c-zz81QtKI','https://www.youtube.com/watch?v=3c-zz81QtKI','2023-11-09 06:00:29','2023-11-09 06:08:17',1,0,1,1),(89,'   8:53 / 20:11   【GOD】Lエヴァを救いたいｗｗ','YouTube','https://www.youtube.com/watch?v=3c-zz81QtKI','','2023-11-09 06:08:48','2024-10-29 15:45:26',0,0,1,1),(90,'https://www.youtube.com/watch?v=3c-zz81QtKI','YouTube','https://www.youtube.com/embed/3c-zz81QtKI','','2023-11-09 06:09:53','2023-11-09 06:09:53',0,0,1,1),(91,'ホワイトノイズ','YouTube','https://www.youtube.com/embed/_ciQX22n9NE&list=RDAMVMR2UiaXn9_J8','','2023-11-09 06:11:56','2023-11-09 06:11:56',0,0,1,1),(92,'【解説】「ひずみ」の蓄積は？南海トラフ地震の想定震源域 海底で海上保安庁が進める地殻変動観測『週刊地震ニュース』','YouTube','https://www.youtube.com/embed/qg44KzxSeXg','【解説】「ひずみ」の蓄積は？南海トラフ地震の想定震源域 海底で海上保安庁が進める地殻変動観測『週刊地震ニュース』','2023-11-09 06:13:44','2023-11-09 06:13:44',0,0,1,1),(93,'スクショ','スクリーンショット 2023-12-11 22.06.00_2jWQkBM.png','/media//スクリーンショット 2023-12-11 22.06.00_2jWQkBM.png','','2023-12-15 16:05:47','2023-12-15 16:05:47',0,0,1,1),(94,'Red Hot Chili Peppers - Show Me Your Soul','YouTube','https://www.youtube.com/embed/XAqSmB1-ecY','Official Music Video for Show Me Your Soul performed by Red Hot Chili Peppers.\r\nFollow Red Hot Chili Peppers: \r\n\r\nInstagram:   / chilipeppers  \r\nFacebook:   / chilipeppers  \r\nTwitter:   / chilipeppers  \r\nWebsite: https://redhotchilipeppers.com/\r\n\r\n#RedHotChiliPeppers #ShowMeYourSoul\r\n\r\nhttp://vevo.ly/WpLJf4','2024-06-12 14:27:20','2024-06-12 16:11:55',0,0,1,1),(95,'しんしゅうかん','001 2024-06-11 08_38_02.jpg','/media//001 2024-06-11 08_38_02.jpg','緑の芝生に囲まれた円形の庭があり、中央には建物が配置されています。建物は独特のデザインで、柱が立ち並び、緑の植物が絡まっています。遠くには、ガラスの構造物が特徴的な屋根の一部が見えます。青い空と白い雲が広がり、明るい日差しの下で静かな雰囲気を醸し出しています。庭には小さな木や草が生え、そこから曲がった歩道が見えます。','2024-08-14 02:07:52','2024-08-24 07:48:16',0,0,1,1),(96,'IMG_1680.HEIC','IMG_1680.HEIC','/Users/syun1/dev/archive_system_django/media/uploads/IMG_1680.HEIC',NULL,'2024-10-29 15:05:38','2024-10-29 15:05:38',0,1,0,1),(97,'IMG_1662.HEIC','IMG_1662.HEIC','/Users/syun1/dev/archive_system_django/media/uploads/IMG_1662.HEIC',NULL,'2024-10-29 15:05:38','2024-10-29 15:05:38',0,1,0,1),(98,'IMG_1664.HEIC','IMG_1664.HEIC','/Users/syun1/dev/archive_system_django/media/uploads/IMG_1664.HEIC',NULL,'2024-10-29 15:05:38','2024-10-29 15:05:38',0,1,0,1),(99,'IMG_1688.jpeg','IMG_1688.jpeg','/Users/syun1/dev/archive_system_django/media/uploads/IMG_1688.jpeg',NULL,'2024-10-29 15:07:53','2024-10-29 15:09:25',1,1,0,1),(100,'IMG_1687.jpeg','IMG_1687.jpeg','/Users/syun1/dev/archive_system_django/media/uploads/IMG_1687.jpeg',NULL,'2024-10-29 15:07:53','2024-10-29 15:09:25',1,1,0,1),(101,'IMG_1688.jpeg','IMG_1688.jpeg','/Users/syun1/dev/archive_system_django/media/uploads/IMG_1688.jpeg',NULL,'2024-10-29 15:10:14','2024-10-29 15:10:14',0,1,0,1),(102,'ファイル','IMG_1688.jpeg','/media/uploads/IMG_1688.jpeg','夜間の街のシーンが映し出されている画像です。2台のバイクが並んで停まっています。左側にはクルーザータイプのバイクがあり、クロームのフレームや長めのフォークが特徴です。フロントヘッドライトが目立ち、黄色いヘルメットがハンドルに掛かっています。右側にはスポーツタイプのバイクがあり、白いヘルメットが取り付けられています。周囲には街灯があり、背景には建物や車の姿が見えます。全体的に暗い中で、バイクが明るい部分に位置しています。','2024-10-29 15:12:23','2024-10-29 15:14:39',0,1,1,1);
/*!40000 ALTER TABLE `upload` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-01  1:31:07
