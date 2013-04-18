from flask import Blueprint, request
from flask.helpers import make_response

from moxie.core.representations import HALRepresentation
from .views import Search


def create_blueprint(blueprint_name):
    contact_blueprint = Blueprint(blueprint_name, __name__)

    contact_blueprint.add_url_rule('/', view_func=get_routes)

    contact_blueprint.add_url_rule('/search',
                                   view_func=Search.as_view('search'))
    return contact_blueprint


def get_routes():
    path = request.path
    representation = HALRepresentation({})
    representation.add_curie('hl', 'http://moxie.readthedocs.org/en/latest/http_api/contact.html#{rel}')
    representation.add_link('self', '{bp}'.format(bp=path))
    representation.add_link('hl:search', '{bp}search?q={{q}}&medium={{medium}}'.format(bp=path),
                            templated=True, title='Search')
    response = make_response(representation.as_json(), 200)
    response.headers['Content-Type'] = "application/json"
    return response