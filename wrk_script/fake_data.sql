delimiter $$
DROP PROCEDURE IF EXISTS create_user_data$$
create procedure create_user_data(startuid INT,step INT)

begin
START TRANSACTION;
SET @uid=startuid;
SET @enduid = startuid + step;
WHILE @uid < @enduid DO

SET @password = 'e10adc3949ba59abbe56e057f20f883e';
SET @picture = 'http://r47q6lm7l.hn-bkt.clouddn.com/11639993218235';
SET @username = CONCAT(@uid);
SET @nickname = CONCAT(@uid);

INSERT INTO test.entry_task_user(`id`, `username`, `password`, `nickname`, `picture`) VALUES(@uid, @username, @password, @nickname, @picture);

SET @uid=@uid+1;
end while ;
COMMIT;
end$$
delimiter ;
