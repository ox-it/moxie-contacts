import logging

from flask import request

from moxie.core.views import ServiceView, accepts
from moxie.core.representations import JSON, HAL_JSON
from moxie.core.cache import cache, args_cache_key
from moxie.core.exceptions import BadRequest
from moxie_contacts.services import ContactSearchService
from moxie_contacts.representations import HALPersonsRepresentation

logger = logging.getLogger(__name__)


class Search(ServiceView):

    AUTHORIZED_MEDIUMS = ('phone', 'email')

    @cache.cached(timeout=60, key_prefix=args_cache_key)
    def handle_request(self):
        q = request.args.get('q', None)
        medium = request.args.get('medium', None)
        if not q or not medium:
            raise BadRequest("Parameters 'q' (query) and 'medium' ('phone' or 'email') are mandatory.")
        if medium not in Search.AUTHORIZED_MEDIUMS:
            raise BadRequest("'medium' should be one of '{}'.".format(', '.join(Search.AUTHORIZED_MEDIUMS)))
        provider = ContactSearchService.from_context()
        results = provider.search(q, medium)
        return {'results': results, 'q': q, 'medium': medium}

    @accepts(HAL_JSON, JSON)
    def as_hal_json(self, response):
        return HALPersonsRepresentation(response['results'], response['q'], response['medium'],
                                        request.url_rule.endpoint).as_json()