from time import sleep

from wikipedia import celery_app
from wikipedia.constants import POPULATION_EXCEED_ERROR, AREA_EXCEED_ERROR, DICT_TASK_NAME
from dbconnect import session_scope
from wikipedia.models import Country, Continent
from error_logger import error_logger


def get_all_countries_data() -> list:
    """
    Gets information related to all countries

    :returns: returns dict of info related to all companies
    :rtype: dict
    """
    list_countries = []
    with session_scope() as session:
        countries = session.query(Country)
        for country in countries:
            dict_country = {
                'country_id': country.country_id,
                'name': country.name,
                'population': country.population,
                'area': country.area,
                'hospitals': country.hospitals,
                'national_parks': country.national_parks,
                'continent': country.continent.name
            }
            list_countries.append(dict_country)
    return list_countries


def get_country_data(
        country_id: int
) -> dict:
    """
    Get data for input country id
    :param country_id: Country's id
    :type country_id: int

    :return: returns dict of country details for given input id
    :rtype: dict
    """
    with session_scope() as session:
        country = session.query(Country).filter(Country.country_id == country_id).one_or_none()
        if not country:
            return {}

        return {
            'country_id': country.country_id,
            'name': country.name,
            'population': country.population,
            'area': country.area,
            'hospitals': country.hospitals,
            'national_parks': country.national_parks,
            'continent': country.continent.name
        }


@celery_app.task
def add_country_data(
        dict_input: dict
) -> str:
    """
    Adds the country to the database.
    :param dict_input: Input parameters with country's attribute
    :type dict_input: dict

    :return: returns Message with insert status
    :rtype: str
    """
    country = Country(
        name=dict_input['name'],
        population=dict_input['population'],
        area=dict_input['area'],
        continent_id=dict_input['continent_id'],
        hospitals=dict_input['hospitals'],
        national_parks=dict_input['national_parks']
    )
    with session_scope() as session:
        try:
            continent = session.query(Continent).\
                filter(Continent.continent_id == dict_input['continent_id']).one_or_none()
            if not continent:
                return f"First insert continent with id {dict_input['continent_id']}."
            session.add(country)
            session.commit()
        except Exception as e:
            error_mss = str(e)
            session.rollback()
            if POPULATION_EXCEED_ERROR in error_mss:
                return f"Insert for country {dict_input['name']} with {dict_input['population']} population failed as" \
                       f" it exceeds the population of the continent it belongs to."
            if AREA_EXCEED_ERROR in error_mss:
                return f"Insert for country {dict_input['name']} with {dict_input['area']} area failed as it exceeds" \
                       f" the area of the continent it belongs to."
            error_logger.error(str(e))
            return f"Insert for country {dict_input['name']} failed."
    return f"Country {dict_input['name']} inserted successfully."


@celery_app.task
def update_country_data(
        country_id: int,
        continent_id: int,
        name=None,
        population=None,
        area=None,
        hospitals=None,
        national_parks=None,
) -> str:
    """
    Updates the field's for the specified country id.
    :param country_id: Country's id
    :type country_id: int
    :param country_id: Continent id, defaults to None
    :type country_id: int, optional
    :param name: Name of the country, defaults to None.
    :type name: str, optional
    :param population: Population of that country, defaults to None.
    :type population: int, optional
    :param area: Area of country, defaults to None.
    :type area: int, optional
    :param hospitals: Hospitals in that country, defaults to None.
    :type hospitals: int, optional
    :param national_parks: National parks in that country, defaults to None.
    :type national_parks: int, optional

    :return: returns Message with update status
    :rtype: str
    """
    sleep(60)
    with session_scope() as session:
        try:
            country = session.query(Country).filter(Country.country_id == country_id).one_or_none()
            if not country:
                return f"Country with id {country_id} does not exist."
            if name:
                country.name = name
            if population:
                country.population = population
            if area:
                country.area = area
            if hospitals:
                country.hospitals = hospitals
            if national_parks:
                country.national_parks = national_parks
            if continent_id:
                country.continent_id = continent_id
            session.commit()
        except Exception as e:
            error_mss = str(e)
            session.rollback()
            if POPULATION_EXCEED_ERROR in error_mss:
                return f"Update for country id {country_id} with {population} population failed as it exceeds the" \
                       f" population of the continent it belongs to."
            if AREA_EXCEED_ERROR in error_mss:
                return f"Update for country id {country_id} with {area} area failed as it exceeds the area of" \
                       f" the continent it belongs to."
            error_logger.error(str(e))
            return f"Update for country with id {country_id} failed."
    return f"Update for country with id {country_id} successful."


@celery_app.task
def delete_country_data(
    country_id: int
) -> str:
    """
    Deletes the country as well as cities in that country from the database.
    :param country_id: Country's id
    :type country_id: int

    :return: returns Message with delete status
    :rtype: str
    """
    with session_scope() as session:
        country = session.query(Country).filter(Country.country_id == country_id).one_or_none()
        list_deleted_cities = []
        if country:
            country_name = country.name
            for city in country.cities:
                list_deleted_cities.append(city.name)
            session.delete(country)
            session.commit()
        else:
            return f"Country with id {country_id} does not exist."
    return f"Deleted cities {list_deleted_cities} with country {country_name}."


DICT_TASK_NAME.update({'add_country_data': add_country_data})
DICT_TASK_NAME.update({'update_country_data': update_country_data})
DICT_TASK_NAME.update({'delete_country_data': delete_country_data})
