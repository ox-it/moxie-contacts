import logging

from moxie.core.service import Service


logger = logging.getLogger(__name__)


class ContactSearchService(Service):

    def __init__(self, search_provider_config=None):
        self.searcher = self._import_provider(search_provider_config.items()[0])

    def search(self, query, medium, match):
        """Search in provider
        :param query: query
        :param medium: medium (email, tel)
        :param match: match (exact, approximate)
        :return: list of domain objects
        """
        return self.searcher.search(query, medium, match)