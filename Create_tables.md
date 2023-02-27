# Sql commands to recrate tables

### Users table:
```SQL
CREATE TABLE `db`.`users` (`id` INT NOT NULL AUTO_INCREMENT , `date_insert` TEXT NOT NULL , `date_update` TEXT NOT NULL , `phone` TEXT NOT NULL , `password_hash` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
```
### Users_tokens table:
```SQL
CREATE TABLE `db`.`users_tokens` (`id` INT NOT NULL AUTO_INCREMENT , `date_insert` TEXT NOT NULL , `date_update` TEXT NOT NULL , `user_id` INT NOT NULL , `token` TEXT NOT NULL , `expires` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
```