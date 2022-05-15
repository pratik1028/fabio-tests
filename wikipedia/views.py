from celery.result import AsyncResult
from flask import request
from error_logger import error_logger
from wikipedia import flask_app
from wikipedia.city import get_all_cities_data, get_city_data, add_city_data, update_city_data, delete_city_data
from wikipedia.constants import BAD_REQUEST, INTERNAL_SERVER, TASK_MESSAGE, DICT_TASK_NAME
from wikipedia.continent import get_all_continents_data, delete_continent_data, get_continent_data, \
    add_continent_data, update_continent_data
from wikipedia.country import get_all_countries_data, get_country_data, add_country_data, update_country_data, \
    delete_country_data
from wikipedia.utils import http_json_response


@flask_app.route("/tasks", methods=['GET'])
def get_status():
    """
    Gets the status of async task running.
    :return:
    """
    task_id = request.args.get('task_id')
    task_name = request.args.get('task_name')
    if not task_id or not task_name:
        return http_json_response(
            message="Mandatory parameter missing.",
            status_code=BAD_REQUEST,
            error=True
        )
    if task_name not in DICT_TASK_NAME:
        return http_json_response(
            message=f"Task {task_name} is not valid."
        )
    task_result = DICT_TASK_NAME[task_name].AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return http_json_response(result)


"""
    CONTINENT API's
"""


@flask_app.route('/get_all_continents', methods=['GET'])
def get_all_continents():
    """
    API to get all continents in database.
    """
    try:
        continents = get_all_continents_data()
        return http_json_response(continents)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/get_continent', methods=['GET'])
def get_continent():
    """
    API to get details for given continent id.
    """
    try:
        continent_id = request.args.get('continent_id')
        if not continent_id:
            return http_json_response(
                message="Mandatory parameter continent_id missing.",
                status_code=BAD_REQUEST,
                error=True
            )
        continent = get_continent_data(int(continent_id))
        if not continent:
            return http_json_response(
                message=f"Continent with id {continent_id} does not exist."
            )
        return http_json_response(continent)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/add_continent', methods=['POST'])
def add_continent():
    """
    API to insert a continent in database.
    """
    try:
        input_params = request.get_json()
        if not input_params.get('name') or \
                not input_params.get('population') or \
                not input_params.get('area'):
            return http_json_response(
                message="Mandatory parameters missing",
                status_code=BAD_REQUEST,
                error=True
            )
        task = add_continent_data.apply_async(
            args=[input_params],
            queue='WIKI_QUEUE'
        )
        message = TASK_MESSAGE.format(task.id, 'add_continent_data')
        return http_json_response(data=task.id, message=message)
        # mess = add_continent_data(input_params)
        # return http_json_response(message=mess)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/update_continent', methods=['PUT'])
def update_continent():
    """
    API to update the fields of given continent id
    """
    try:
        input_params = request.get_json()
        continent_id = input_params.get('continent_id')
        name = input_params.get('name')
        area = input_params.get('area')
        population = input_params.get('population')
        if not continent_id:
            return http_json_response(
                message="Mandatory parameter continent_id missing",
                status_code=BAD_REQUEST,
                error=True
            )
        if not area and not population and not name:
            return http_json_response(
                message="Provide atleast one field to update.",
                status_code=BAD_REQUEST,
                error=True
            )
        task = update_continent_data.apply_async(
            args=[continent_id, name, population, area],
            queue='WIKI_QUEUE'
        )
        message = TASK_MESSAGE.format(task.id, 'update_continent_data')
        return http_json_response(data=task.id, message=message)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/delete_continent', methods=['DELETE'])
def delete_continent():
    """
    API to delete the given continent id
    """
    try:
        continent_id = request.args.get('continent_id')
        if not continent_id:
            return http_json_response(
                message="Mandatory parameter continent_id missing",
                status_code=BAD_REQUEST,
                error=True
            )
        task = delete_continent_data.apply_async(
            args=[int(continent_id)],
            queue='WIKI_QUEUE'
        )
        message = TASK_MESSAGE.format(task.id, 'delete_continent_data')
        return http_json_response(data=task.id, message=message)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


"""
    COUNTRY API's
"""


@flask_app.route('/get_all_countries', methods=['GET'])
def get_all_countries():
    """
    API to get all countries in database.
    """
    try:
        countries = get_all_countries_data()
        return http_json_response(countries)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/get_country', methods=['GET'])
def get_country():
    """
    API to get details for given country id.
    """
    try:
        country_id = request.args.get('country_id')
        if not country_id:
            return http_json_response(
                message="Mandatory parameter country_id missing.",
                status_code=BAD_REQUEST,
                error=True
            )
        country = get_country_data(int(country_id))
        if not country:
            return http_json_response(
                message=f"Country with id {country_id} does not exist."
            )
        return http_json_response(country)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/add_country', methods=['POST'])
def add_country():
    """
    API to insert a country in database.
    """
    try:
        input_params = request.get_json()
        if not input_params.get('continent_id'):
            return http_json_response(
                message="Mandatory parameters continent_id missing.",
                status_code=BAD_REQUEST,
                error=True
            )
        if not input_params.get('name') or \
                not input_params.get('population') or \
                not input_params.get('area'):
            return http_json_response(
                message="Mandatory parameters missing",
                status_code=BAD_REQUEST,
                error=True
            )
        task = add_country_data.apply_async(
            args=[input_params],
            queue='WIKI_QUEUE'
        )
        message = TASK_MESSAGE.format(task.id, 'add_country_data')
        return http_json_response(data=task.id, message=message)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/update_country', methods=['PUT'])
def update_country():
    """
    API to update the fields of given country id
    """
    try:
        input_params = request.get_json()
        country_id = input_params.get('country_id')
        continent_id = input_params.get('continent_id')
        name = input_params.get('name')
        area = input_params.get('area')
        national_parks = input_params.get('national_parks')
        hospitals = input_params.get('hospitals')
        population = input_params.get('population')
        if not country_id:
            return http_json_response(
                message="Mandatory parameter missing.",
                status_code=BAD_REQUEST,
                error=True
            )
        if not area and not population and not name and not continent_id:
            return http_json_response(
                message="Provide atleast one field to update.",
                status_code=BAD_REQUEST,
                error=True
            )
        task = update_country_data.apply_async(
            args=[country_id, continent_id, name, population, area, hospitals, national_parks],
            queue='WIKI_QUEUE'
        )
        message = TASK_MESSAGE.format(task.id, 'update_country_data')
        return http_json_response(data=task.id, message=message)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/delete_country', methods=['DELETE'])
def delete_country():
    """
    API to delete the given country id
    """
    try:
        country_id = request.args.get('country_id')
        if not country_id:
            return http_json_response(
                message="Mandatory parameter missing",
                status_code=BAD_REQUEST,
                error=True
            )
        task = delete_country_data.apply_async(
            args=[int(country_id)],
            queue='WIKI_QUEUE'
        )
        message = TASK_MESSAGE.format(task.id, 'delete_country_data')
        return http_json_response(data=task.id, message=message)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


"""
    CITY API's
"""


@flask_app.route('/get_all_cities', methods=['GET'])
def get_all_cities():
    """
    API to get all cities in database.
    """
    try:
        cities = get_all_cities_data()
        return http_json_response(cities)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/get_city', methods=['GET'])
def get_city():
    """
    API to get details for given city id.
    """
    try:
        city_id = request.args.get('city_id')
        if not city_id:
            return http_json_response(
                message="Mandatory parameter city_id missing.",
                status_code=BAD_REQUEST,
                error=True
            )
        city = get_city_data(int(city_id))
        if not city:
            return http_json_response(
                message=f"City with id {city_id} does not exist."
            )
        return http_json_response(city)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/add_city', methods=['POST'])
def add_city():
    """
    API to insert a city in database.
    """
    try:
        input_params = request.get_json()
        if not input_params.get('country_id'):
            return http_json_response(
                message="Mandatory parameters continent_id missing.",
                status_code=BAD_REQUEST,
                error=True
            )
        if not input_params.get('name') or \
                not input_params.get('population') or \
                not input_params.get('area'):
            return http_json_response(
                message="Mandatory parameters missing",
                status_code=BAD_REQUEST,
                error=True
            )
        task = add_city_data.apply_async(
            args=[input_params],
            queue='WIKI_QUEUE'
        )
        message = TASK_MESSAGE.format(task.id, 'add_city_data')
        return http_json_response(data=task.id, message=message)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/update_city', methods=['PUT'])
def update_city():
    """
    API to update the fields of given continent id
    """
    try:
        input_params = request.get_json()
        city_id = input_params.get('city_id')
        country_id = input_params.get('country_id')
        name = input_params.get('name')
        area = input_params.get('area')
        roads = input_params.get('roads')
        trees = input_params.get('trees')
        population = input_params.get('population')
        if not city_id:
            return http_json_response(
                message="Mandatory parameter city_id missing.",
                status_code=BAD_REQUEST,
                error=True
            )
        if not area and not population and not name and not country_id:
            return http_json_response(
                message="Provide atleast one field to update.",
                status_code=BAD_REQUEST,
                error=True
            )
        task = update_city_data.apply_async(
            args=[city_id, country_id, name, population, area, roads, trees],
            queue='WIKI_QUEUE'
        )
        message = TASK_MESSAGE.format(task.id, 'update_city_data')
        return http_json_response(data=task.id, message=message)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )


@flask_app.route('/delete_city', methods=['DELETE'])
def delete_city():
    """
    API to delete the given city id
    """
    try:
        city_id = request.args.get('city_id')
        if not city_id:
            return http_json_response(
                message="Mandatory parameter city_id missing",
                status_code=BAD_REQUEST,
                error=True
            )
        task = delete_city_data.apply_async(
            args=[int(city_id)],
            queue='WIKI_QUEUE'
        )
        message = TASK_MESSAGE.format(task.id, 'delete_city_data')
        return http_json_response(data=task.id, message=message)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )
