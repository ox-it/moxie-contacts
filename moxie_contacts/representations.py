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


class HALPersonRepresentation(PersonRepresentation):

    def __init__(self, person, endpoint):
        """HAL  representation for an item
        :param item: domain item to represent
        :param endpoint: base endpoint (URL)
        """
        super(HALPersonRepresentation, self).__init__(person)
        self.endpoint = endpoint

    def as_dict(self):
        base = super(HALPersonRepresentation, self).as_dict()
        representation = HALRepresentation(base)
        representation.add_link('self', url_for(self.endpoint))
        return representation.as_dict()

    def as_json(self):
        return jsonify(self.as_dict())