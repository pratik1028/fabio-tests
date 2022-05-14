-- TRIGER UPDATE COUNTRY
DELIMITER $$
CREATE TRIGGER before_country_update
    BEFORE UPDATE
	ON `country` FOR EACH ROW
	BEGIN
	    SET @flag = "false";
	    SET @error_msg = "";
	    IF old.population <> new.population THEN
		    SET @error_msg = "POPULATION ERROR";
		    CALL check_total_population_continent(new.continent_id, new.country_id, new.population, @flag);
	    END IF;
	    IF old.area <> new.area THEN
		    SET @error_msg = "AREA ERROR";
		    CALL check_total_area_continent(new.continent_id, new.country_id, new.area, @flag);
	    END IF;
	    IF @flag="true" THEN
	    SIGNAL SQLSTATE '45000'
	    SET MESSAGE_TEXT = @error_msg;
	    END IF;
	END; $$

-- TRIGER INSERT COUNTRY
DELIMITER $$
CREATE TRIGGER before_country_insert
    BEFORE INSERT
	ON `country` FOR EACH ROW
	BEGIN
	    SET @flag = "false";
	    SET @error_msg = "POPULATION ERROR";
	    CALL check_total_population_continent(new.continent_id, new.country_id, new.population, @flag);
	    IF @flag="true" THEN
	    SIGNAL SQLSTATE '45000'
	    SET MESSAGE_TEXT = @error_msg;
	    END IF;
	    SET @error_msg = "AREA ERROR";
	    CALL check_total_area_continent(new.continent_id, new.country_id, new.area, @flag);
	    IF @flag="true" THEN
	    SIGNAL SQLSTATE '45000'
	    SET MESSAGE_TEXT = @error_msg;
	    END IF;
	END; $$

-- PROCEDURE POPULATION CONTINENT
DELIMITER &&
CREATE  PROCEDURE check_total_population_continent(IN continentid INT, IN countryid INT, IN new_population INT, OUT flag VARCHAR(5))
BEGIN
SELECT IF(
		(SELECT IFNULL(SUM(population),0) + new_population
		 FROM country
		 WHERE continent_id = continentid
		 AND country_id <> countryid) >
		 (SELECT population
		 FROM continent
		 WHERE continent_id = continentid), "true", "false"
          )
 INTO flag;
END &&

-- PROCEDURE AREA CONTINENT
DELIMITER &&
CREATE  PROCEDURE check_total_area_continent(IN continentid INT, IN countryid INT, IN new_area INT, OUT flag VARCHAR(5))
BEGIN
SELECT IF(
		(SELECT IFNULL(SUM(`area`),0) + new_area
		 FROM country
		 WHERE continent_id = continentid
		 AND country_id <> countryid) >
		 (SELECT `area`
		 FROM continent WHERE continent_id = continentid), "true", "false"
          )
 INTO flag;
END &&

-- TRIGER UPDATE CITY
DELIMITER $$
CREATE TRIGGER before_city_update
    BEFORE UPDATE
	ON `city` FOR EACH ROW
	BEGIN
	    SET @flag = "false";
	    SET @error_msg = "";
	    IF old.population <> new.population THEN
		    SET @error_msg = "POPULATION ERROR";
		    CALL check_total_population_country(new.country_id, new.city_id, new.population, @flag);
	    END IF;
	    IF old.area <> new.area THEN
		    SET @error_msg = "AREA ERROR";
		    CALL check_total_area_country(new.country_id, new.city_id, new.area, @flag);
	    END IF;
	    IF @flag="true" THEN
	    SIGNAL SQLSTATE '45000'
	    SET MESSAGE_TEXT = @error_msg;
	    END IF;
	END; $$

-- TRIGGER INSERT CITY
DELIMITER $$
CREATE TRIGGER before_city_insert
    BEFORE INSERT
	ON `city` FOR EACH ROW
	BEGIN
	    SET @flag = "false";
	    SET @error_msg = "POPULATION ERROR";
	    CALL check_total_population_country(new.country_id, new.city_id, new.population, @flag);
	    IF @flag="true" THEN
	    SIGNAL SQLSTATE '45000'
	    SET MESSAGE_TEXT = @error_msg;
	    END IF;
	    SET @error_msg = "AREA ERROR";
	    CALL check_total_area_country(new.country_id, new.city_id, new.area, @flag);
	    IF @flag="true" THEN
	    SIGNAL SQLSTATE '45000'
	    SET MESSAGE_TEXT = @error_msg;
	    END IF;
	END; $$

-- PROCEDURE POPULATION COUNTRY
DELIMITER &&
CREATE  PROCEDURE check_total_population_country (IN countryid INT, IN cityid INT, IN new_population INT, OUT flag VARCHAR(5))
BEGIN
SELECT IF(
		(SELECT IFNULL(SUM(population),0) + new_population
		 FROM city
		 WHERE country_id = countryid
		 AND city_id <> cityid) >
		 (SELECT population

		 FROM country WHERE country_id = countryid), "true", "false"
          )
 INTO flag;
END &&

-- PROCEDURE AREA COUNTRY
DELIMITER &&
CREATE  PROCEDURE check_total_area_country (IN countryid INT, IN cityid INT, IN new_area INT, OUT flag VARCHAR(5))
BEGIN
SELECT IF(
		(SELECT IFNULL(SUM(`area`),0) + new_area
		 FROM city
		 WHERE country_id = countryid
		 AND city_id <> cityid) >
		 (SELECT `area`
		 FROM country WHERE country_id = countryid), "true", "false"
          )
 INTO flag;
END &&