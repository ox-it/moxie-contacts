from flask import url_for, jsonify

from moxie.core.representations import Representation, HALRepresentation


class PersonRepresentation(Representation):

    def __init__(self, person):
        self.person = person

    def as_dict(self):
        values = {
            'name': self.person.name,
            'unit': self.person.unit,
            }
        if self.person.email:
            values['email'] = self.person.email
        if self.person.internal_tel:
            values['internal_tel'] = self.person.internal_tel
        if self.person.external_tel:
            values['external_tel'] = self.person.external_tel
        return values

    def as_json(self):
        return jsonify(self.as_dict())


class PersonsRepresentation(Representation):

    def __init__(self, persons):
        self.persons = persons

    def as_dict(self):
        return {'persons': [PersonRepresentation(person).as_dict()
                            for person in self.persons]}

    def as_json(self):
        return jsonify(self.as_dict())


class HALPersonsRepresentation(PersonsRepresentation):

    def __init__(self, persons, query, medium, endpoint):
        self.endpoint = endpoint
        self.query = query
        self.medium = medium
        self.persons = persons

    def as_dict(self):
        persons = PersonsRepresentation(self.persons).as_dict()
        representation = HALRepresentation(persons)
        representation.add_link('self', url_for(self.endpoint, q=self.query, medium=self.medium))
        return representation.as_dict()

    def as_json(self):
        return jsonify(self.as_dict())