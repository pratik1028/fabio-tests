from dbconnect import session_scope
from wikipedia.models import Continent
from error_logger import error_logger


def get_all_continents_data() -> list:
    """
    Gets information related to all continents

    :returns: returns dict of info related to all companies
    :rtype: dict
    """
    list_continents = []
    with session_scope() as session:
        continents = session.query(Continent)
    for continent in continents:
        dict_continent = {
            'continent_id': continent.continent_id,
            'name': continent.name,
            'population': continent.population,
            'area': continent.area
        }
        list_continents.append(dict_continent)
    return list_continents


def get_continent_data(
        continent_id: int
) -> dict:
    """
    Get data for input continent id
    :param continent_id: Continents id
    :type continent_id: int

    :return: returns dict of continent details for given input id
    :rtype: dict
    """
    with session_scope() as session:
        continent = session.query(Continent).filter(Continent.continent_id == continent_id).one_or_none()
        if not continent:
            return {}

    return {
        'continent_id': continent.continent_id,
        'name': continent.name,
        'population': continent.population,
        'area': continent.area
    }


def add_continent_data(
        dict_input: dict
) -> str:
    """
    Adds the continent to the database.
    :param dict_input: Input paramters with continent's attribute
    :type dict_input: dict

    :return: returns Message with insert status
    :rtype: str
    """
    continent = Continent(
        name=dict_input['name'],
        population=dict_input['population'],
        area=dict_input['area']
    )
    with session_scope() as session:
        session.add(continent)
        session.commit()
    return f"Continent {dict_input['name']} inserted successfully."


def update_continent_data(
        continent_id: int,
        name=None,
        population=None,
        area=None,
) -> str:
    """
    Updates the field's for the specified continent id.
    :param continent_id: Continent's id
    :type continent_id: int
    :param name: Name of the continent, defaults to None.
    :type name: str, optional
    :param population: Population of that continent, defaults to None.
    :type population: int, optional
    :param area: Area of continent, defaults to None.
    :type area: int, optional

    :return: returns Message with update status
    :rtype: str
    """
    with session_scope() as session:
        try:
            continent = session.query(Continent).filter(Continent.continent_id == continent_id).one_or_none()
            if not continent:
                return f"Continent with id {continent_id} does not exist."
            if name:
                continent.name = name
            if population:
                continent.population = population
            if area:
                continent.area = area
            session.commit()
        except Exception as e:
            error_logger.error(str(e))
            session.rollback()
            return f"Update for continent with id {continent_id} failed."
    return f"Update for continent with id {continent_id} successful."


def delete_continent_data(
        continent_id: int
) -> str:
    """
    Deletes the continent from the database.
    :param continent_id: Continent's id
    :type continent_id: int

    :return: returns Message with delete status
    :rtype: str
    """
    with session_scope() as session:
        continent = session.query(Continent).filter(Continent.continent_id == continent_id).one_or_none()
        list_deleted_countries = []
        list_deleted_cities = []
        if continent:
            continent_name = continent.name
            for country in continent.countries:
                list_deleted_countries.append(country.name)
                for city in country.cities:
                    list_deleted_cities.append(city.name)
            session.delete(continent)
            session.commit()
        else:
            return f"Continent with id {continent_id} does not exist."
    return f"Deleted countries {list_deleted_cities} and cities {list_deleted_countries}" \
           f" with continent {continent_name}."
