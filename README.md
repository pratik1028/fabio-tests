## Assignment
This is mini wikipidea which provides features to Create, Read, 
Update and Delete on geographical entities data.

###Approach

####Database Design
Three tables created continents, countries and cities to hold the 
geographical data

1. Continent<br />
   continent_id(pk), name(uk), population, area, created, updated.
2. Country<br />
   country_id(pk), continent_id(fk), name(uk), population, area, 
   hospitals, national_parks, created, updated.
3. City<br />
   city_id(pk), country_id(fk), name(uk), population, area, 
   roads, trees, created, updated.<br/>


