CREATE DATABASE authentication;

CREATE TABLE login (
id_user int primary key AUTO_INCREMENT,
username varchar(50) not null,
number_registration VARCHAR(5) UNIQUE,
passw varchar(60) not null,
fingerprint_image LONGBLOB

)ENGINE=InnoDB DEFAULT CHARSET=utf8;