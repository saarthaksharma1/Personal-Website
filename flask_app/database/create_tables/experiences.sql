CREATE TABLE IF NOT EXISTS `experiences` (
    `experience_id`      int(11)       NOT NULL AUTO_INCREMENT COMMENT 'PK: The experience id',
    `position_id`        int(11)       NOT NULL                COMMENT 'FK: The position id',
    `name`               varchar(100)  NOT NULL                COMMENT 'The name of this experience',
    `description`        varchar(500)  NOT NULL                COMMENT 'The description of this experience',
    `hyperlink`          varchar(500)  NOT NULL                COMMENT 'The link where people can learn more about the experience',
    `start_date`         date          DEFAULT NULL                COMMENT 'My start date for this experience',
    `end_date`           date          DEFAUlT NULL                COMMENT 'The end date for this experience',
    PRIMARY KEY (`experience_id`),
    FOREIGN KEY (position_id) REFERENCES positions(position_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Experiences I have had at each position";
