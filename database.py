import sqlite3

class Database:
    def __init__(self, database_path):
        self.conn = None
        self.database_path = database_path
        self.sqls = {'create': 'create table if not exists {} ({})',
                     'insert': 'insert into {} values({})',
                     'select': 'select {} from {}'}

    def commit(self):
        if self.conn:
            self.conn.commit()

    def create(self, table, cols):
        cols = ','.join([col[0] + ' ' + col[1] for col in cols])
        sql_create = self.sqls['create'].format(table, cols)

        self.get_connection()
        self.conn.execute(sql_create)

    def get_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.database_path,
                                        isolation_level=None,
                                        check_same_thread=False)

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def insert(self, table, values):
        values = [value for value in values]
        sql_insert = self.sqls['insert'].format(table, ','.join(['?']*len(values)))

        self.get_connection()
        self.conn.execute(sql_insert, values)

    def select(self, table, cols, is_conditional=False, condition=None):
        sql_select = self.sqls['select'].format(','.join(cols), table)
        self.get_connection()
        rows = self.conn.execute(sql_select)
        return [row for row in rows]
