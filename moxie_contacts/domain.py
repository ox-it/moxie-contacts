class Person(object):

    def __init__(self, name, unit, email=None, internal_tel=None, external_tel=None):
        self.name = name
        self.unit = unit
        self.email = email
        self.internal_tel = internal_tel
        self.external_tel = external_tel