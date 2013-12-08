import sqlite3

class DataStore:
    conns = {}
    sqls = {'create': 'create table if not exists {} ({})',
            'insert': 'insert into {} values({})'}

    @classmethod
    def get_connection(cls, database):
        if database not in cls.conns:
            conn = sqlite3.connect(database)
            cls.conns[database] = conn
        return cls.conns[database]

    @classmethod
    def create(cls, database, table, cols):
        conn = cls.get_connection(database)
        conn.execute(cls.sqls['create'])

    @classmethod
    def insert(cls, database, table, values):
        conn = cls.get_connection(database)
        conn.execute(cls.sqls['insert'])

