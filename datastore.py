import sqlite3

class DataStore:
    conns = {}
    sqls = {'create': 'create table if not exists {} ({})',
            'insert': 'insert into {} values({})'}

    @classmethod
    def get_connection(cls, database):
        if database not in cls.conns:
            conn = sqlite3.connect(database, check_same_thread=False)
            cls.conns[database] = conn
        return cls.conns[database]

    @classmethod
    def create(cls, database, table, cols):
        conn = cls.get_connection(database)
        cols = ','.join([col[0] + ' ' + col[1] for col in cols])
        sql_create = cls.sqls['create'].format(table, cols)
        print sql_create
        conn.execute(sql_create)

    @classmethod
    def close(cls, database):
        if database in cls.conns:
            cls.conns[database].close()
            cls.conns.pop(database)

    @classmethod
    def insert(cls, database, table, values):
        conn = cls.get_connection(database)
        values = [value.decode('utf-8') for value in values]
        sql_insert = cls.sqls['insert'].format(table, ','.join(['?']*len(values)))
        conn.execute(sql_insert, values)
        conn.commit()

