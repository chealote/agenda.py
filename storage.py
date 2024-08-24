import sqlite3

from os import path
from queryConstructor import QueryConstructor as qc
from log import Log, LogLevel

def last_index_of(string, char):
    if len(char) != 1:
        raise Exception("char should be a single char long")
    for c in range(len(string)-1, -1, -1):
        if string[c] == char:
            return c
    return -1

class Storage:
    def __init__(self, for_class, log=None):
        scriptpath = path.realpath(path.abspath(__file__))
        scriptdir = scriptpath[0:last_index_of(scriptpath, "/")+1]
        self.__db_filepath = scriptdir + "agenda.db"
        self.__table_desc = for_class

        self.__log = log

    def __enter__(self):
        self.__conn = sqlite3.connect(self.__db_filepath)
        self.__cur = self.__conn.cursor()
        self.__try_create_table(self.__table_desc)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__conn.close()

    def __try_create_table(self, cls):
        query = qc.gen_create_table_query(cls)
        self.__cur.execute(query)
        self.__conn.commit()

    def insert(self, item):
        query = qc.insert_new_item(item)
        self.__log.debug(f"insert query: {query}")
        self.__cur.execute(query)
        self.__conn.commit()

    def delete(self, item):
        query = qc.gen_delete(item)
        self.__log.debug(f"delete query: {query}")
        self.__cur.execute(query)
        self.__conn.commit()

    def filter_between(self, item, key, between_args):
        query = qc.gen_select_filter_between(item, key, between_args)
        self.__log.debug(f"running {query}")
        self.__cur.execute(query, ())
        return self.__cur.fetchall()

    def filter_key_values(self, item, key_values):
        query = qc.gen_select_filter_keyvalues(item, key_values)
        self.__log.debug(f"running {query}")
        self.__cur.execute(query, ())
        return self.__cur.fetchall()


    def select_all(self, item):
        query = qc.gen_select_all(item)
        self.__log.debug(f"running {query}")
        self.__cur.execute(query, ())
        return self.__cur.fetchall()
