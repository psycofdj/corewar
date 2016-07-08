USE `${mysql:database}`;

CREATE TABLE `ship`
(
        `id`          int(11)      NOT NULL auto_increment,
        `name`        varchar(512) NOT NULL,
        `date`        datetime     NOT NULL,
        `compiles`    int(11)      NOT NULL,
        `code`        longtext     NOT NULL,

        PRIMARY KEY (`id`),
        UNIQUE KEY (`name`(200))
) ENGINE=InnoDB  DEFAULT CHARACTER SET utf8 COLLATE utf8_bin AUTO_INCREMENT=1;


CREATE TABLE `user_ship`
(
   `uid` int(11) NOT NULL,
   `sid` int(11) NOT NULL,

   FOREIGN KEY (`uid`) REFERENCES `user`(id) ON DELETE CASCADE,
   FOREIGN KEY (`sid`) REFERENCES `ship`(id) ON DELETE CASCADE
) ENGINE=InnoDB  DEFAULT CHARACTER SET binary AUTO_INCREMENT=1;

INSERT INTO `ship` (`id`, `name`, `date`, `compiles`, `code`)
       VALUES (1, "test", NOW(), 1, ".name \"test\"
.comment \"This is the first ship ever.\"

  ll r0, 0x2ecf       # Load simple code
  ll r1, 0x13e0       #   into two registers
  ll r2, to -from1    # Load offsets for
  ll r3, to -from2 +4 #   the two str
  str [r2], r0        # Write code just
from1:
  str [r3], r1        # before PC
from2:
to:                   # When the PC reaches here , a check
                      # instruction has been written");

INSERT INTO `user_ship` (`uid`, `sid`)
       VALUES (1, 1);
