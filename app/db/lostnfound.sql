/* Create our database */
CREATE DATABASE lostnfound CHARACTER SET utf8;

/* Setup permissions for the server */
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'adminpassword';
GRANT ALL ON lostnfound.* TO 'admin'@'localhost';


/* Permissions for using Docker DBs */
CREATE USER 'admin'@'172.17.0.1' IDENTIFIED BY 'adminpassword';
GRANT ALL ON lostnfound.* TO 'admin'@'172.17.0.1';
