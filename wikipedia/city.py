from time import sleep

from wikipedia import celery_app
from wikipedia.constants import POPULATION_EXCEED_ERROR, AREA_EXCEED_ERROR, DICT_TASK_NAME
from dbconnect import session_scope
from wikipedia.models import City, Country
from error_logger import error_logger


def get_all_cities_data() -> list:
    """
    Gets information related to all cities

    :returns: returns dict of info related to all cities
    :rtype: dict
    """
    list_cities = []
    with session_scope() as session:
        cities = session.query(City)
        for city in cities:
            dict_city = {
                'city_id': city.city_id,
                'name': city.name,
                'population': city.population,
                'area': city.area,
                'roads': city.roads,
                'trees': city.trees,
                'country': city.country.name
            }
            list_cities.append(dict_city)
    return list_cities


def get_city_data(
        city_id: int
) -> dict:
    """
    Get data for input city id
    :param city_id: City's id
    :type city_id: int

    :return: returns dict of city details for given input id
    :rtype: dict
    """
    with session_scope() as session:
        city = session.query(City).filter(City.city_id == city_id).one_or_none()
        if not city:
            return {}

        return {
            'city_id': city.city_id,
            'name': city.name,
            'population': city.population,
            'area': city.area,
            'roads': city.roads,
            'trees': city.trees,
            'country': city.country.name
        }


@celery_app.task
def add_city_data(
        dict_input: dict
) -> str:
    """
    Adds the city to the database.
    :param dict_input: Input parameters with city's attribute
    :type dict_input: dict

    :return: returns Message with insert status
    :rtype: str
    """
    city = City(
        name=dict_input['name'],
        population=dict_input['population'],
        area=dict_input['area'],
        country_id=dict_input['country_id'],
        roads=dict_input['roads'],
        trees=dict_input['trees']
    )
    with session_scope() as session:
        try:
            country = session.query(Country).filter(Country.country_id == dict_input['country_id']).one_or_none()
            if not country:
                return f"First insert country with id {dict_input['country_id']}."
            session.add(city)
            session.commit()
        except Exception as e:
            error_mss = str(e)
            session.rollback()
            if POPULATION_EXCEED_ERROR in error_mss:
                return f"Insert for city {dict_input['name']} with {dict_input['population']} population failed as" \
                       f" it exceeds the population of the country it belongs to."
            if AREA_EXCEED_ERROR in error_mss:
                return f"Insert for city {dict_input['name']} with {dict_input['area']} area failed as it exceeds" \
                       f" the area of the country it belongs to."
            error_logger.error(str(e))
            return f"Insert for city {dict_input['name']} failed."
    return f"City {dict_input['name']} inserted successfully."


@celery_app.task
def update_city_data(
        city_id: int,
        country_id=None,
        name=None,
        population=None,
        area=None,
        roads=None,
        trees=None,
) -> str:
    """
    Updates the field's for the specified city id.
    :param city_id: City's id
    :type city_id: int
    :param city_id: Country id defaults to None.
    :type city_id: int, optional
    :param name: Name of the city, defaults to None.
    :type name: str, optional
    :param population: Population of that city, defaults to None.
    :type population: int, optional
    :param area: Area of city, defaults to None.
    :type area: int, optional
    :param trees: Hospitals in that city, defaults to None.
    :type trees: int, optional
    :param roads: National parks in that city, defaults to None.
    :type roads: int, optional

    :return: returns Message with update status
    :rtype: str
    """
    sleep(60)
    with session_scope() as session:
        try:
            city = session.query(City).filter(City.city_id == city_id).one_or_none()
            if not city:
                return f"City with id {city_id} does not exist."
            if name:
                city.name = name
            if population:
                city.population = population
            if area:
                city.area = area
            if roads:
                city.roads = roads
            if trees:
                city.national_parks = trees
            if country_id:
                city.country_id = country_id
            session.commit()
        except Exception as e:
            error_mss = str(e)
            session.rollback()
            if POPULATION_EXCEED_ERROR in error_mss:
                return f"Update for city id {city_id} with {population} population failed as it exceeds the" \
                       f" population of the country it belongs to."
            if AREA_EXCEED_ERROR in error_mss:
                return f"Update for city id {city_id} with {area} area failed as it exceeds the area of" \
                       f" the country it belongs to."
            error_logger.error(str(e))
            session.rollback()
            return f"Update for city with id {city_id} failed."
    return f"Update for city with id {city_id} successful."


@celery_app.task
def delete_city_data(
    city_id: int,
) -> str:
    """
    Deletes the city as well as cities in that city from the database.
    :param city_id: City's id
    :type city_id: int

    :return: returns Message with delete status
    :rtype: str
    """
    with session_scope() as session:
        city = session.query(City).filter(City.city_id == city_id).one_or_none()
        if city:
            city_name = city.name
            session.delete(city)
            session.commit()
        else:
            return f"City with id {city_id} does not exist."
    return f"Deleted city {city_name}."


DICT_TASK_NAME.update({'add_city_data': add_city_data})
DICT_TASK_NAME.update({'update_city_data': update_city_data})
DICT_TASK_NAME.update({'delete_city_data': delete_city_data})
