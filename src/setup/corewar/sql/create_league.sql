USE `${mysql:database}`;

CREATE TABLE `time_results`
(
   `id`       int(11)       NOT NULL auto_increment,
   `uid`      int(11)       NOT NULL,
   `name`     varchar(512)  NOT NULL,
   `code`     longtext      NOT NULL,
   `hash`     varchar(256)  NOT NULL,
   `log`      longtext      NOT NULL,
   `finished` int(11)       NOT NULL,
   `cycles`   int(11)       NOT NULL,
   `date`     datetime      NOT NULL,

   PRIMARY KEY (`id`),
   FOREIGN KEY (`uid`) REFERENCES `user`(id)   ON DELETE CASCADE,
   UNIQUE KEY (hash(200))
) ENGINE=InnoDB  DEFAULT CHARACTER SET utf8 COLLATE utf8_bin AUTO_INCREMENT=1;

