import sqlite3
import threading

class Database:
    def __init__(self, database_path):
        self.conns = dict()
        self.database_path = database_path
        self.sqls = {'create': 'create table if not exists {} ({})',
                     'insert': 'insert into {} values({})',
                     'select': 'select {} from {}'}

    # def commit(self, thread_name):
    #     if thread_name in self.conns:
    #         self.conns[thread_name].commit()

    def create(self, table, cols):
        cols = ','.join([col[0] + ' ' + col[1] for col in cols])
        sql_create = self.sqls['create'].format(table, cols)

        conn = sqlite3.connect(self.database_path)
        conn.execute(sql_create)
        conn.close()

    def get_connection(self, thread_name):
        if thread_name in self.conns:
            return self.conns[thread_name]
        else:
            conn = sqlite3.connect(self.database_path, timeout=10)
            self.conns[thread_name] = conn
            return conn

    # def close(self, thread_name):
    #     if thread_name in self.conns:
    #         self.conns[thread_name].close()
    #         self.conns.pop(thread_name)

    def insert(self, table, values):
        thread_name = threading.current_thread().name
        values = [value for value in values]
        sql_insert = self.sqls['insert'].format(table, ','.join(['?']*len(values)))
        conn = self.get_connection(thread_name)
        conn.execute(sql_insert, values)
        conn.commit()

    def select(self, table, cols):
        sql_select = self.sqls['select'].format(','.join(cols), table)
        conn = sqlite3.connect(self.database_path)
        rows = conn.execute(sql_select)
        result = [row for row in rows]
        conn.close()
        return result

    def record_failure(self, sql):
        with open('data/failed_sqls.txt', 'a') as file_:
            file_.write(self.database_path + ' : ' + sql + '\n')
