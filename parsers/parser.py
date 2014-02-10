class Parser(object):
    def __init__(self):
        assert hasattr(self, 'name'), '%s must have a name' % type(self).__name__

    def __str__(self):
        return self.name

    def set_database(self, database):
        self.database = database
