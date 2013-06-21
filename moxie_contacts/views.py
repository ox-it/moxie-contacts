import logging

from flask import request

from moxie.core.views import ServiceView, accepts
from moxie.core.representations import JSON, HAL_JSON
from moxie.core.exceptions import BadRequest
from moxie_contacts.services import ContactSearchService
from moxie_contacts.representations import HALPersonsRepresentation

logger = logging.getLogger(__name__)


class Search(ServiceView):

    AUTHORIZED_MEDIUMS = ('phone', 'email')

    def handle_request(self):
        self.q = request.args.get('q', None)
        self.medium = request.args.get('medium', None)
        if not self.q or not self.medium:
            raise BadRequest("Parameters 'q' (query) and 'medium' ('phone' or 'email') are mandatory.")
        if self.medium not in Search.AUTHORIZED_MEDIUMS:
            raise BadRequest("'medium' should be one of '{}'.".format(', '.join(Search.AUTHORIZED_MEDIUMS)))
        provider = ContactSearchService.from_context()
        results = provider.search(self.q, self.medium)
        return results

    @accepts(HAL_JSON, JSON)
    def as_hal_json(self, results):
        return HALPersonsRepresentation(results, self.q, self.medium,
                                        request.url_rule.endpoint).as_json()