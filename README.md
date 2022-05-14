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
<br/><br/>
#### API Design
Used Flask framework for creating GET, POST, PUT and DELETE API's and SQLAlchemy for ORM.<br/><br/>
Created following API's:
1. **Continent**:
   1. ``GET /get_all_continents HTTP/1.1``
   2. ``GET /get_continent?continent_id=4 HTTP/1.1``
   3. ``POST /add_continent HTTP/1.1>``<br/> ``Body: {"name": "asia",
                  "population": 100, "area": 100}``
   4. ``PUT /update_continent HTTP/1.1
`` <br/>``Body:{"continent_id": 1, "population": 1000, "area": 10}``
   5. ``DELETE /delete_continent?continent_id=3 HTTP/1.1
``
2. **Country**:
   1. ``GET /get_all_counties HTTP/1.1``
   2. ``GET /get_country?country_id=1 HTTP/1.1``
   3. ``POST /add_country HTTP/1.1>``<br/> ``Body: {"name": "india", "population": 50, "area": 50, "continent_id": 1, "hospitals": 50, "national_parks": 25}
``
   4. ``PUT /update_country HTTP/1.1
`` <br/>``Body:{"country_id":1, "population": 25, "area": 25}``
   5. ``DELETE /delete_country?country_id=1 HTTP/1.1
``
3. City:
   1. ``GET /get_all_cities HTTP/1.1``
   2. ``GET /get_city?city_id=1 HTTP/1.1``
   3. ``POST /add_city HTTP/1.1>``<br/> ``Body: {"name": "mumbai", "population": 20, "area": 25, "country_id": 2, "roads": 50, "trees": 25}
``
   4. ``PUT /update_city HTTP/1.1
`` <br/>``Body:{"city_id": 1, "population": 40, "area": 5}
``
   5. ``DELETE /delete_continent?continent_id=3 HTTP/1.1
``


