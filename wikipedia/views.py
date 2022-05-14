from flask import request
from error_logger import error_logger
from wikipedia import flask_app
from wikipedia.constants import BAD_REQUEST, INTERNAL_SERVER
from wikipedia.continent import get_all_continents_data, delete_continent_data, get_continent_data, add_continent_data, \
    update_continent_data
from wikipedia.utils import http_json_response

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
    API to get details for given continent.
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
                message=f"Conitnent with id {continent_id} does not exist."
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
        insert_mess = add_continent_data(input_params)
        return http_json_response(message=insert_mess)
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
        update_mss = update_continent_data(
            continent_id=continent_id,
            name=name,
            population=population,
            area=area,
        )
        return http_json_response(message=update_mss)
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
        delete_mess = delete_continent_data(int(continent_id))
        return http_json_response(message=delete_mess)
    except Exception as e:
        error_logger.error(str(e))
        return http_json_response(
            message=str(e),
            status_code=INTERNAL_SERVER
        )
