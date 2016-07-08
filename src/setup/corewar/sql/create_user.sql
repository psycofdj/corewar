USE `${mysql:database}`;

CREATE TABLE `user`
(
        `id` int(11)                NOT NULL auto_increment,
        `name`        varchar(512)  NOT NULL,
        `nickname`    varchar(512)  NOT NULL,
        `mail`        varchar(512)  NOT NULL,
        `password`    varchar(512)  NOT NULL,

        PRIMARY KEY (`id`),
        UNIQUE KEY (`mail`(200)),
        UNIQUE KEY (`name`(200)),
        UNIQUE KEY (`nickname`(200))
) ENGINE=InnoDB  DEFAULT CHARACTER SET utf8 COLLATE utf8_bin AUTO_INCREMENT=1;


INSERT INTO `user` (`id`, `name`, `nickname`, `mail`, `password`)
VALUES
        (1, 'Xavier MARCELET', 'PsYcO-X[fDj]', 'xavier@marcelet.com', SHA2('dduyg8kn', 512));
