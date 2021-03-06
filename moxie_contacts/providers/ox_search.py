import logging
import re

import requests
from lxml import etree

from moxie.core.exceptions import ServiceUnavailable
from requests.exceptions import RequestException
from moxie_contacts.domain import Person

logger = logging.getLogger(__name__)


class ContactProvider(object):
    """University's contact search API
    """

    # See http://en.wikipedia.org/wiki/Nobility_particle for more information.
    _NOBILITY_PARTICLES = set([
        'de', 'van der', 'te', 'von', 'van', 'du', 'di'
    ])

    def __init__(self, url):
        """Contact search provider for the University of Oxford
        :param url: URL of the service
        """
        self.api_url = url

    def search(self, query, medium, match):
        """Search in the provider
        :param query: search query
        :param medium: medium (phone or email)
        :param exact: whether to search for exact matches. If False, search is approximate.
        :return: list of domain objects
        """
        normalized = self.normalize_query(query, medium, match)
        results = self.perform_query(normalized['surname'], normalized['initial'],
                                     normalized['medium'], normalized['match'])
        return results

    def normalize_query(self, query, medium, match):
        # Examples of initial / surname splitting
        # William Bloggs is W, Bloggs
        # Bloggs         is  , Bloggs
        # W Bloggs       is W, Bloggs
        # Bloggs W       is W, Bloggs
        # Bloggs William is B, William
        parts = query.split(' ')
        parts = [p for p in parts if p]
        i = 0

        while i < len(parts)-1:
            if parts[i].lower() in ContactProvider._NOBILITY_PARTICLES:
                parts[i:i+2] = [' '.join(parts[i:i+2])]
            elif parts[i] == '':
                parts[i:i+1] = []
            else:
                i += 1

        parts = parts[:2]
        if len(parts) == 0:
            surname, initial = None, None
        elif len(parts) == 1:
            surname, initial = parts[0], None
        elif parts[0].endswith(','):
            surname, initial = parts[0][:-1], parts[1][:1]
        elif len(parts[1]) == 1:
            surname, initial = parts[0], parts[1]
        else:
            surname, initial = parts[1], parts[0][:1]

        return {
            'surname': surname,
            'initial': initial,
            'medium': medium,
            'match': match,
            }

    def perform_query(self, surname, initial, medium, match):
        query_string = ';'.join('%s=%s' % i for i in (
            ('surname', re.sub(r"[^A-Za-z\-']", '', surname or '')),
            ('initial',re.sub(r"[^A-Za-z\-']", '', initial or '')),
            ('match', match),
            ('type', medium),
        ))

        try:
            response = requests.get('{}?{}'.format(self.api_url, query_string),
                                    timeout=2)
            response.raise_for_status()
        except RequestException:
            logger.error("Couldn't reach {url}".format(url=self.api_url,),
                         exc_info=True)
            raise ServiceUnavailable()
        else:
            x_people = etree.fromstring(response.content)
            people = []
            for x_person in x_people.findall('person'):
                name = x_person.find('name').text
                unit = x_person.find('unit' if medium == 'email' else 'dept').text
                person = Person(name, unit)

                if medium == 'email':
                    person.email = x_person.find('email').text

                if medium == 'phone':
                    person.internal_tel = x_person.find('phone_from_in').text
                    person.external_tel = x_person.find('phone_from_out').text
                people.append(person)
            return people