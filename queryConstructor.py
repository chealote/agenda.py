import re
import inspect

from log import Log

class QueryConstructor:
    def __search_tupple(item, dict_name):
        values = None
        try:
            for members in inspect.getmembers(item):
                if members[0] == dict_name:
                    values = members[1]
            return values
        except IndexError:
            return None

    def __search_tablename_from_item(instance):
        return QueryConstructor.__search_tupple(instance, "__class__").__name__.lower()

    def __remove_last_element(string, elem):
        if string == "":
            return string
        # TODO replace this with "\s+,\s+$" or something
        if string[-1] == ",":
            return string[:-1]
        return re.sub(r"(.*)(\s*"+elem+"\s*)", r"\1", string)

    def gen_create_table_query(cls):
        annos = QueryConstructor.__search_tupple(cls, "__annotations__")

        col_defs = ""
        for anno in annos:
            prop = ""
            if anno == "id":
                prop = "PRIMARY KEY AUTOINCREMENT"
            col_defs += f" {anno} {QueryConstructor.__map_type_sqlite(annos[anno])} {prop},"
            prop = ""

        col_defs = QueryConstructor.__remove_last_element(col_defs, ",")

        tablename = cls.__name__.lower()
        return f"CREATE TABLE IF NOT EXISTS {tablename} \
({col_defs})"

    def __map_type_sqlite(typ):
        if typ == str:
            return "TEXT"
        if typ == int:
            return "INTEGER"
        return "TEXT"

    def insert_new_item(item, include_id=False):
        dic = QueryConstructor.__search_tupple(item, "__dict__")
        tablename = QueryConstructor.__search_tablename_from_item(item)
        cols = ""
        values = ""
        for key in dic:
            if "id" == key and not include_id:
                continue
            cols += f"{key},"
            if type(dic[key]) == str:
                values += f"'{dic[key]}',"
            else:
                values += f"{dic[key]},"

        cols = QueryConstructor.__remove_last_element(cols, ",")
        values = QueryConstructor.__remove_last_element(values, ",")
        return f"INSERT INTO {tablename}({cols}) VALUES ({values})"

    def gen_select_all(like_class):
        dic = QueryConstructor.__search_tupple(like_class, "__annotations__")
        # tablename = QueryConstructor.__search_tablename_from_item(like_class)
        cols = ""
        for key in dic:
            cols += f"{key},"
        cols = QueryConstructor.__remove_last_element(cols, ",")
        return f"SELECT {cols} FROM {like_class.__name__}"

    def gen_select_filter_between(like_item, filter_key, between_values, hardcoded=""):
        query = QueryConstructor.gen_select_all(like_item)
        query += f" WHERE {filter_key} BETWEEN '{between_values[0]}' AND '{between_values[1]}'"
        # TODO hardcoded? find a better way to do this
        query += hardcoded
        # TODO custom ordering, should be customizable or another function
        query += f" ORDER BY {filter_key} ASC"
        return query

    def gen_select_filter_keyvalues(like_item, key_values):
        query = QueryConstructor.gen_select_all(like_item)
        query += " WHERE"
        for key in key_values:
            query += f" {key}='{key_values[key]}' AND "
        query = QueryConstructor.__remove_last_element(query, "AND")
        print("QUERY:", query)
        return query

    def gen_delete(like_item):
        dic = QueryConstructor.__search_tupple(like_item, "__dict__")
        tablename = QueryConstructor.__search_tablename_from_item(like_item)
        where_clause = f"DELETE FROM {tablename} WHERE "
        for key in dic:
            if type(dic[key]) == list:
                where_clause += f"{key} IN ("
                for v in dic[key]:
                    where_clause += f"'{v}', "
                where_clause = QueryConstructor.__remove_last_element(where_clause, ",")
                where_clause += ")"
            else:
                where_clause += f"{key}='{dic[key]}' AND "
        where_clause = QueryConstructor.__remove_last_element(where_clause, "AND")
        return where_clause

if __name__ == "__main__":
    class Event:
        id:int
        description:str
        date_time:str
        tags: list

    class Person:
        name:str
        email:str

    log = Log()

    event = Event()
    qc = QueryConstructor
    log.info(qc.gen_create_table_query(Event))

    event.id = 123
    event.description = "A new thing I need to do"
    event.datetime = 12
    log.info(qc.insert_new_item(event))
    log.info(qc.gen_select_all(Event))
    log.info(qc.gen_select_filter_between(Event, "date_time", ("date1", "date2")))
    log.info(qc.gen_delete(event))

    person = Person()
    log.info(qc.gen_create_table_query(Person))

    person.name = "Ale"
    person.email = "some@email.com"

    log.info(qc.insert_new_item(person))
    log.info(qc.gen_select_all(Person))

    e = Event()
    e.tags = [1,2,3,4,5]
    log.info(qc.gen_delete(e))

# e = Events()
# e.id = 1
# e.description = "Something"
# query = qc.generateInsert(e)
# db.execute(query)
