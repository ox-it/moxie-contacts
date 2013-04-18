import logging

from flask import request, abort

from moxie.core.views import ServiceView, accepts
from moxie.core.representations import JSON, HAL_JSON
from moxie_contacts.services import ContactSearchService
from moxie_contacts.representations import HALPersonRepresentation

logger = logging.getLogger(__name__)


class Search(ServiceView):

    def handle_request(self):
        # 1. Request from Service
        self.q = request.args.get('q', None)
        self.medium = request.args.get('medium', None)
        provider = ContactSearchService.from_context()
        results = provider.search(self.q, self.medium)
        return results

    @accepts(HAL_JSON, JSON)
    def as_hal_json(self, results):
        return HALPersonRepresentation(results[0], request.url_rule.endpoint).as_json()