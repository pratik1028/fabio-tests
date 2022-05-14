## Assignment
This is mini wikipidea which provides features to Create, Read, 
Update and Delete on geographical entities data.

###Approach

####Database Design
Three tables created continents, countries and cities to hold the 
geographical data.

1. Continent<br />
   continent_id(pk), name(uk), population, area, created, updated.
2. Country<br />
   country_id(pk), continent_id(fk), name(uk), population, area, 
   hospitals, national_parks, created, updated.
3. City<br />
   city_id(pk), country_id(fk), name(uk), population, area, 
   roads, trees, created, updated.<br/>

Refer: ``fabio-tests/dbscripts/tables.sql``
    
Added following validation logic using **Trigger** and **Procedure**:

1. Population/area of newly **inserted** country cannot be greater that population/area
of continent it belongs to.<br/>
2. Population/area of newly **inserted** city cannot be greater that population/area
of country.<br/>
3. Population/area of **updated** country cannot be greater that population/area
of continent it belongs to.<br/>
4. Population/area of **upaded** city cannot be greater that population/area
of country.<br/>
   
**Trigger** on country table:<br/>`before_country_insert` and `before_country_update`
which called **procedures** `check_total_population_continent` and `check_total_area_continent` to get if new population/area
is less than continent.

**Trigger** on city table:<br/>`before_city_insert` and `before_city_update`
which called **procedures** `check_total_population_country` and `check_total_area_country` to get if new population/area
is less than country.<br/>

Refer: ``fabio-tests/dbscripts/trigger_and_procedure.sql``
